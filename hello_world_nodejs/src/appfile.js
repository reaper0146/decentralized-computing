const filecoin = require("filecoin");

//import { HttpJsonRpcConnector, LotusClient } from 'filecoin.js';

(async () => {

  const connector = new filecoin.HttpJsonRpcConnector({ url: __LOTUS_RPC_ENDPOINT__, token: __LOTUS_AUTH_TOKEN__ });

  const jsonRpcProvider = new LotusClient(httpConnector);
  const version = await jsonRpcProvider.common.version();
  console.log(version);

})().then().catch();