import fs from 'fs';

console.log('running party-to-list.js')

const list = [];

fs.readdirSync('../../partijwebsite-lijsten').forEach(file => {
    const data = JSON.parse(fs.readFileSync(`../../partijwebsite-lijsten/${file}`, 'utf8'));

    list.push(...data)
});

fs.writeFileSync('../../partijwebsite-lijsten/list.json', JSON.stringify(list, null, 2), 'utf8');