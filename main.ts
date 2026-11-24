// Entry program for make.fun's "Promote make.fun's make-your-own-bounty
// post on X" bounty (program/v1). Its whole job: copy POST.json -- the
// address of our post on X -- from this repository to /output, unchanged.
// The house reads the post itself and writes its counts beside the copy.
import { copyFileSync, mkdirSync } from "node:fs";

const here = new URL(".", import.meta.url);
mkdirSync("/output", { recursive: true });
copyFileSync(new URL("POST.json", here), "/output/POST.json");
console.log("POST.json copied to /output");
