import { FlureeClient } from '@fluree/fluree-client';

// for node < 18 (glibc < 2.28)
import fetch from 'node-fetch';
global.fetch = fetch;

const client = await new FlureeClient({
    isFlureeHosted: true,
    apiKey: process.env.FLUREE_API_KEY,
    // host: 'localhost',
    // port: 58090,
    // create: true, // this is not idempotent
    ledger: 'fluree-jld/387028092978542',
}).connect();

client.generateKeyPair();
const privateKey = client.getPrivateKey();
client.setKey(privateKey);

// unsigned query
let query = client
    .query({
        select: { freddy: ['*'] },
    });
console.log(query)

// this works
let response = await query.send();
console.log(response)

// this does not (signed query)
let signedQuery = query.sign();
console.log(signedQuery);
// fails with 400 Bad Request
response = await signedQuery.send();
console.log(response)
