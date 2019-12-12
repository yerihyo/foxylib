#!/bin/bash -eu

POST https://api.github.com/repos/yerihyo/foxylib/releases

{
  "tag_name": "v0.3.74",
  "target_commitish": "develop",
  "name": "v0.3.74",
  "body": "Release",
  "draft": false,
  "prerelease": false
}
