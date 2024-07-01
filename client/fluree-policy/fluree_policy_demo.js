/*
The script demonstrates how to work with Fluree policy features. The script
makes use of Fluree JS client: https://github.com/fluree/fluree-client
and connects to a local Fluree server.

Covered operations:
* policy configuration
* role-based querying
* identity-based querying

Limitations:
* ledger clean-up is not covered. You need to set new `ledgerName` for 
  subsequent script calls

Execution:
$ node fluree_policy_demo.js

data source: https://discord.com/channels/896089675511508992/1245329089343262720/1245521794589266051
*/
import { FlureeClient } from '@fluree/fluree-client';

// for node < 18 (glibc < 2.28)
import fetch from 'node-fetch';
global.fetch = fetch;


const ledgerName = 'fluree/fluree-policy-demo8';

(async () => {
    const client = await new FlureeClient({
        host: 'localhost',
        port: 58090,
        create: true, // this is not idempotent
        ledger: ledgerName,
    }).connect();
    console.log(client);

    client.generateKeyPair();
    const privateKey = client.getPrivateKey();
    client.setKey(privateKey);
    const did = client.getDid();
    console.log(did);

    const dataTransaction = {
        "ledger": ledgerName,
        "@context": {
            "ex": "http://example.org/"
        },
        "insert": [
            {
                "age": 35,
                "name": "Souma Mukerjee",
                "@type": "Person",
                "@id": "2"
            },
            {
                "age": 36,
                "name": "Souradeep Das",
                "@type": "Person",
                "@id": "3"
            },
            {
                "age": 24,
                "name": "Tanmay Kumar",
                "@type": "Person",
                "@id": "ex:Tanmay"
            }
        ]
    };
    let response1 = await client.transact(dataTransaction).send();
    console.log(response1);

    let policyTransaction = {
        "ledger": ledgerName,
        "@context": {
            "ex": "http://example.org/",
            "f": "https://ns.flur.ee/ledger#"
        },
        insert: [
            {  // associate caller with the ex:Tanmay user having ex:nameViewRole role
                "@id": did,
                "ex:user": { "@id": "ex:Tanmay" },
                "f:role": { "@id": "ex:nameViewRole" }
            },
            {
                "@id": "ex:NameViewPolicy",
                "@type": ["f:Policy"],
                "f:targetClass": { "@id": "Person" },
                "f:allow": [
                    {  // everyone with ex:nameViewRole can view any Person data
                        "@id": "ex:nameViewAllow",
                        "f:targetRole": { "@id": "ex:nameViewRole" },
                        "f:action": [{ "@id": "f:view" }]
                    }
                ],
                "f:property": [
                    {  // a caller can view only their own age
                        "@id": "ex:subsOnlyViewName",
                        "f:path": { "@id": "age" },
                        "f:allow": [
                            {
                                "@id": "ex:ageViewRule",
                                "f:targetRole": { "@id": "ex:nameViewRole" },
                                "f:action": [{ "@id": "f:view" }],
                                "f:equals": {
                                    "@list": [{ "@id": "f:$identity" }, { "@id": "ex:user" }]
                                }
                            }
                        ]
                    }
                ]
            }]
    };
    let response2 = await client.transact(policyTransaction).send();
    console.log(response2);

    let queryWithoutPolicyApplied = {
        "@context": {
            "ex": "http://example.org/"
        },
        "from": ledgerName,
        "select": {  // get all people data
            "?person": [
                "*"
            ]
        },
        "where": {
            "@id": "?person",
            "@type": "Person"
        }
    };
    let response3 = await client.query(queryWithoutPolicyApplied).send();
    // notice that age of all people is visible
    console.log(response3);

    let queryWithPolicyAppliedRole = {
        "@context": {
            "ex": "http://example.org/"
        },
        "from": ledgerName,
        "select": {
            "?person": [
                "*"
            ]
        },
        "where": {
            "@id": "?person",
            "@type": "Person"
        },
        "opts": {
            "role": "ex:nameViewRole"
        }
    };
    let response4 = await client.query(queryWithPolicyAppliedRole).send();
    // notice that ex:Tanmay can't see age of other people (ex:People)
    console.log(response4);

    let queryWithPolicyAppliedDid = {
        "@context": {
            "ex": "http://example.org/"
        },
        "from": ledgerName,
        "select": {
            "?person": [
                "*"
            ]
        },
        "where": {
            "@id": "?person",
            "@type": "Person"
        },
        "opts": {
            "did": did
        }
    };
    let response5 = await client.query(queryWithPolicyAppliedDid).send();
    // same output as for role-based querying
    console.log(response5);
})();