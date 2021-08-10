import os
import sys
import json
iexec_out = os.environ['IEXEC_OUT']
iexec_in = os.environ['IEXEC_IN']

sys.path.insert(0, iexec_in + '/private-code-dataset')
import private_code

private_code.main()


print("POST Private code operations")

# Declare everything is computed
with open(iexec_out + '/determinism.txt', 'w+') as fout:
    fout.write("It is deterministic.")
with open(iexec_out + '/computed.json', 'w+') as f:
    json.dump({ "deterministic-output-path" : iexec_out + '/determinism.txt' }, f)

print("END")
print("----------------------------")
