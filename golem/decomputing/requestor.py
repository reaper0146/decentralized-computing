#!/usr/bin/env python3
"""
This file contains the requestor part of our application. There are three areas here:
1. Splitting the data into multiple tasks, each of which can be executed by a provider.
2. Defining what commands must be run within the provider's VM.
3. Scheduling the tasks via a yagna node running locally.
"""

import argparse
import asyncio
from datetime import timedelta
import json
import math
from pathlib import Path
from tempfile import gettempdir
from typing import AsyncIterable, Iterator
from uuid import uuid4

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm

import worker

# CLI arguments definition
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--hash", type=Path, default=Path("data/hash.json"))
arg_parser.add_argument("--subnet", type=str, default="devnet-beta.2")
arg_parser.add_argument("--words", type=Path, default=Path("data/words.txt"))

# Container object for parsed arguments
args = argparse.Namespace()

ENTRYPOINT_PATH = "/golem/entrypoint/worker.py"
TASK_TIMEOUT = timedelta(minutes=10)


def data(words_file: Path, chunk_size: int = 100_000) -> Iterator[Task]:
    """Split input data into chunks, each one being a single `Task` object.

    A single provider may compute multiple tasks.
    Return an iterator of `Task` objects.
    """
    with words_file.open() as f:
        chunk = []
        for line in f:
            chunk.append(line.strip())
            if len(chunk) == chunk_size:
                yield Task(data=chunk)
                chunk = []
        if chunk:
            yield Task(data=chunk)


async def steps(context: WorkContext, tasks: AsyncIterable[Task]):
    """Prepare a sequence of steps which need to happen for a task to be computed.

    `WorkContext` is a utility which allows us to define a series of commands to
    interact with a provider.
    Tasks are provided from a common, asynchronous queue.
    The signature of this function cannot change, as it's used internally by `Executor`.
    """
    context.send_file(str(args.hash), worker.HASH_PATH)

    async for task in tasks:
        context.send_json(worker.WORDS_PATH, task.data)

        context.run(ENTRYPOINT_PATH)

        # Create a temporary file to avoid overwriting incoming results
        output_file = Path(gettempdir()) / str(uuid4())
        try:
            context.download_file(worker.RESULT_PATH, str(output_file))

            # Pass the prepared sequence of steps to Executor
            yield context.commit()

            # Mark task as accepted and set its result
            with output_file.open() as f:
                task.accept_result(result=json.load(f))
        finally:
            # Remove output file once it's no longer required
            if output_file.exists():
                output_file.unlink()


async def main():

    # Set of parameters for the VM run by each of the providers
    package = await vm.repo(
        image_hash="581ca2369db1dc93b78e5489d69c24e8134ad54483a8497be5fe0a38",
        min_mem_gib=1.0,
        min_storage_gib=2.0,
    )

    async with Golem(budget=1, subnet_tag=args.subnet) as golem:

        result = ""

        async for task in golem.execute_tasks(
            steps, data(args.words), payload=package, timeout=TASK_TIMEOUT
        ):
            # Every task object we receive here represents a computed task
            if task.result:
                result = task.result
                # Exit early once a matching word is found
                break

        if result:
            print(f"\nFound matching word: {result}\n")
        else:
            print("No matching words found.")


if __name__ == "__main__":
    args = arg_parser.parse_args()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    # yapapi debug logging to a file
    enable_default_logger(log_file="yapapi.log")

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        # Make sure Executor is closed gracefully before exiting
        task.cancel()
        loop.run_until_complete(task)
