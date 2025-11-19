#!/bin/bash
cd android
./gradlew clean
cd ..
npx cap sync android
npx cap run android
