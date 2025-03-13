import { FlureeClient } from '@fluree/fluree-client';

// for node < 18 (glibc < 2.28)
// import fetch from 'node-fetch';
// global.fetch = fetch;

const createLedger = (process.env.CREATE_LEDGER === 'true');
const createData = (process.env.CREATE_DATA === 'true');
const deleteData = createData;
const defaultId = process.env.DEFAULT_ID ? process.env.DEFAULT_ID : 'freddie';
const defaultDepth = process.env.DEFAULT_DEPTH ? process.env.DEFAULT_DEPTH : 2;
const defaultType = process.env.DEFAULT_DEPTH ? process.env.DEFAULT_DEPTH : "Musician";

const client = await new FlureeClient({
    // isFlureeHosted: true,
    // apiKey: process.env.FLUREE_API_KEY,
    host: 'localhost',
    port: 58090,
    ledger: 'fluree-demo/001',
    create: createLedger, // this is not idempotent; use env var CREATE_LEDGER to control
}).connect();

let data = {};
let query = {};
let transaction = {};
let response = {};

/* Data */

data = [ // this can also be just a single non-array object
    {
        "@id": "freddie",
        "@type": "Musician",
        "name": "Freddie",
        "age": 45,
        "plays": { // this can also be enclosed in an array, has no impact on the resulting RDF
            "@id": "vocals",
            "@type": "Instrument",
            "label": "Vocals"
        },
    },
    {
        "@id": "brian",
        "@type": "Musician",
        "name": "Brian",
        "age": 44,
        "plays": {
            "@id": "guitar",
            "@type": "Instrument",
            "label": "Guitar"
        }
    }
];

const childData1 = {
    "plays": { // multiple insertions create lists and so only the queries get array in that case
        "@id": "piano",
        "@type": "Instrument",
        "label": "Piano"
    }
};

const childData2 = {
    "plays": {
        "@id": "drums",
        "@type": "Instrument",
        "label": "Drums"
    }
};

/* DB functions */

const insertData = (data) => {
    return client.transact({
        "insert": data,
    });
}

const insertChildById = (id, data) => {
    return client.transact({
        "insert": {"@id": id, ...data }
    });
}

// this has a side-effect in that any ID existing or not will always yield a (dummy) result
const getById = (id) => {
    return client.query({
        "select": { [id]: ["*"] }
    });
    // will return { "@id": "<id>" } regardless
};

// we can also do explicit ID binding using a special VALUES technique, no side-effect
const getByIdAlternate = (id) => {
    return client.query({
        "selectDistinct": {"?s": ["*"] }, // distinct is required or repeats for every ?p
        // "selectDistinct": "*", // this will return triples not objects
        "where": [{"@id": "?s", "?p": "?o"}],
        "values": ["?s", [{ "@type": "@id", "@value": id }]]
    });
};

// this auto-expanding feature is very Fluree-specific
const getByIdNested = (id, depth) => {
    return client.query({
        "select": { [id]: ["*"] },
        "depth": depth
    });
};

const getAllByType = (type, depth) => {
    return client.query({
        "select": { "?s": ["*"] },
        "where": { "@id": "?s" , "@type": type},
        "depth": depth ? depth : 0
    });
};

/*
* Deletes (child) objects together with all of their incoming relationships
*/
const detachDeleteAllById = (id) => {
    return client.transact({
        "delete": {
            "@id": "?s",
            "?r": {
                "@id": id,
                "?p": "?o"
            }
        },
        "where": {
            "@id": "?s",
            "?r": {
                "@id": id,
                "?p": "?o"
            }
        }
    });
};

// THIS LEAVES ORPHANS
// IF COMMENTED PARTS UNCOMMENTED, WILL DELETE ALL THE DATA!!!
const cascadeDeleteByIdOneLevel = (id) => {
    return client.transact({
        "delete": {
            "@id": id,
            "?p": "?o",
            "?r": {
                // "@id": "?x", // dangerous
                "?rp": "?ro"
            }
        },
        "where": {
            "@id": id,
            "?p": "?o",
            "?r": {
                // "@id": "?x", // dangerous
                "?rp": "?ro"
            }
        }
    });
};

/* Demo functions */

const insertDataDemo = async (data) => {
    transaction = insertData(data);
    console.log("==> TRANSACTION insertData($data)");
    console.log(transaction);
    response = await transaction.send();
    console.log("==> RESPONSE insertData($data)");
    console.log(response);
}

const insertChildByIdDemo = async (id, data) => {
    transaction = insertChildById(id, data);
    console.log("==> TRANSACTION insertChildById($id, $data)");
    console.log(transaction);
    response = await transaction.send();
    console.log("==> RESPONSE insertChildById($id, $data)");
    console.log(response);
}

const getByIdDemo = async (id) => {
    query = getById(id);
    // console.log("==> QUERY getById($id)");
    // console.log(query);
    response = await query.send();
    console.log("==> RESPONSE getById($id)");
    console.log(response);
}

const getByIdAlternateDemo = async (id) => {
    query = getByIdAlternate(id);
    // console.log("==> QUERY getByIdAlternate($id)");
    // console.log(query);
    response = await query.send();
    console.log("==> RESPONSE getByIdAlternate($id)");
    console.log(response);
}

const getByIdNestedDemo = async (id, depth) => {
    query = getByIdNested(id, depth);
    // console.log("==> QUERY getByIdNested($id, $depth<int>)");
    // console.log(query);
    response = await query.send();
    console.log("==> RESPONSE getByIdNested($id, $depth<int>)");
    console.log(JSON.stringify(response, null, 2));
}

const getAllByTypeDemo = async (type, depth) => {
    query = getAllByType(type, depth);
    // console.log("==> QUERY getAllByType($type, $depth<int>[opt])");
    // console.log(query);
    response = await query.send();
    console.log("==> RESPONSE getAllByType($type<int>[opt])");
    console.log(JSON.stringify(response, null, 2));
}

const detachDeleteAllByIdDemo = async (id) => {
    await getByIdDemo(id);
    transaction = detachDeleteAllById(id);
    console.log("==> TRANSACTION detachDeleteAllById($id)");
    console.log(query);
    response = await transaction.send();
    console.log("==> RESPONSE detachDeleteAllById($id)");
    console.log(response);
}

const cascadeDeleteByIdOneLevelDemo = async (id) => {
    transaction = cascadeDeleteByIdOneLevel(id);
    console.log("==> TRANSACTION cascadeDeleteByIdOneLevel($id)");
    console.log(query);
    response = await transaction.send();
    console.log("==> RESPONSE cascadeDeleteByIdOneLevel($id)");
    console.log(response);
}

/* Main */

if (createData) {
    await insertDataDemo(data);
    console.log("RESULT: 2 Musicians, 1 Instrument each");
    console.log();
};

await getByIdDemo(defaultId);
console.log(`RESULT: 1 Musician's flat details (${defaultId}), dummy result possible`);
console.log();
await getByIdAlternateDemo(defaultId);
console.log(`RESULT: 1 Musician's flat details (${defaultId}), no side-effects`)
console.log();
await getByIdNestedDemo(defaultId, defaultDepth);
console.log(`RESULT: 1 Musician's all details (${defaultId}), up to level ${defaultDepth}`)
console.log();
await getAllByTypeDemo(defaultType, defaultDepth);
console.log(`RESULT: All resource's details, of type ${defaultType}`);
console.log();

if (createData) {
    await insertChildByIdDemo(defaultId, childData1);
    console.log();    
    await getByIdNestedDemo(defaultId, defaultDepth);
    console.log(`RESULT: 1 Musician with 1 additional instrument (total 2, 1)`);
    console.log();

    await insertChildByIdDemo(defaultId, childData2);
    console.log();
    await insertChildByIdDemo("brian", childData2);
    console.log();
    await getAllByTypeDemo(defaultType)
    console.log(`RESULT: 2 Musicians with 1 additional instrument each (total 3, 2)`);
    console.log();

    await detachDeleteAllByIdDemo("drums");
    console.log();
    await getAllByTypeDemo(defaultType, defaultDepth);
    console.log(`RESULT: 2 Musicians with 1 instrument removed (total 2, 1)`);
    console.log();

    // does not work
    await cascadeDeleteByIdOneLevelDemo("brian");
    console.log()
    await getAllByTypeDemo(defaultType, defaultDepth);
    console.log(`RESULT: 1 Musician removed with all linked entities`);    
};

await getAllByTypeDemo("Instrument");
console.log(`RESULT: All Instruments left`);
