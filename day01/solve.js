// nodejs solve.js

const input = require("fs").readFileSync("./data.txt", "utf-8").split("\n");

let sum = 0;
let val = 0;
let total = [];

for (i = 0; i < input.length; i++) {
    let line = input[i];

    val = parseInt(line)

    if (isNaN(val)) {
        total.push(sum)
        sum = 0;
    }
    else {
        sum = sum + val;
    }
}

console.log("part1", Math.max( ...total ));

total.sort((a, b) => a - b);

console.log("part2", total.at(-1) + total.at(-2) + total.at(-3))
