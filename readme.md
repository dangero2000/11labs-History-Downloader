# Introduction

## Why?

Eleven Labs has recently introduced a forced arbitration clause into their terms of service agreement, which you can only opt out of by sending certified mail. They snuck this new clause into their Terms of Service earlier in the month of May 2024, and only sent a single email about it, stating that you agree to this clause by continuing to use their service. The new terms go into effect on May 31, last time I checked. I believe there is a 14 day grace period after these new terms go into effect.

I believe this move, along with other moves the company has made in the last few months, has been a huge betrayal of not only my trust, but the trust of other customers who have filled their pockets with money over the past year or so as well - (I was on the $22 Creator Plan). I decided I wasn't going to take this lying down anymore, so I made the move to stop paying for my subscription. I then looked into downloading all the audio clips I'd ever generated with Eleven Labs.

When I searched online about how to download all of my history items, I noticed there wasn't much information available on that subject. I decided to take another look at the terms, and I found this:

> Respect for the privacy and security of your data underpins our approach to responding to data disclosure requests. For more information, please see our Privacy Policy.

This statement is quite confusing. Their respect for your data privacy and security could support their response to data collection requests, but equally, it might not either. Companies like to lie about our privacy and security, and we know that Eleven Labs has no problem with breaking consumer trust. But even if they aren't lying, this statement is so broad that it could mean anything. What is their response when you try to email them about downloading all your data? Will they just hand it over to you, or will they refuse because it goes against their "privacy principles"? What if you're like me, and you used to use Eleven Labs to tell inappropriate jokes privately among your friends? Do they search through all your clips and delete the ones they don't like? After all, they have introduced stricter content policies recently. You could argue that they wouldn't sift through all your content to find something that violates their content policies, but they might not have to. They can already detect when something violates their policies before it reaches the generation process, so what's stopping that same algorithm from searching through past content?

Something that didn't used to be a violation yesterday is a violation today, and they don't let you generate certain things now. Maybe they'd delete your history as well. There's no way of knowing, and I'd rather download my own data from my own account without having to request it and gain the approval of the Eleven Labs team, or trust them to give me all of it after they've already broken our trust multiple times. That's where this project comes in.

## What does it do?

- This is a command line application. You run it and input your Eleven Labs API key.
- You have the option of downloading CSV records of the text you entered to generate each clip, which are ordered by date. This also works with speech-to-speech clips.
- The script will stop after downloading the first 10 audio files and ask if you'd like to continue downloading. This is put in place so that you can check the files to make sure the script is doing what it should.
- At the moment, the application makes CVS files with a maximum of 100 rows to avoid overloading low-spec machines. After the number of rows exceeds 100, it will make a new CSV file.

# Installation and Usage

There are currently no binary releases, so you'll have to run this from source.

## Installation

First, you'll need to make sure you have Python 3 installed. I believe any Python 3.X version will work, but just in case it doesn't, I'm using version 3.11.1 for this project.

Next, make sure you have the right dependencies installed:

```sh
pip install requests
```

Finally, clone the repository:

```sh
git clone https://github.com/dangero2000/11labs-History-Downloader
cd 11labs-history-downloader
```

## Usage

There are 2 ways you can start the program. You can run the script with no arguments, and it'll prompt you to enter your API key:

```sh
python hist.py
```

Alternatively, you can run it with the --api_key argument, and it'll accept your key right away without prompting you for it:

```sh
python hist.py --api_key 'your_api_key_no_quotes'
```

# To due list

- Ask the user how many entries they want in their CVS records before a new one is created
- Add the option to mass delete your history items upon request
- Make the program work with services other than Eleven Labs that also store user data
- Hopefully include dubs, projects, Voice Over Studio, and sound effect generation history

# Known issues

- The application seems to download history items repeatedly at random on a loop, insuring that you never get all of your history. The program runs indefinitely until you use Ctrl C to terminate it. I learned this after running the program over night and coming back to find out it was still downloading things that had already been downloaded and cloning CSV entries.

# I need your help

The truth is, I am a beginner programmer, and definitely do not have enough experience to make a program like this yet. However, I needed something that would download my history before my Eleven Labs subscription expired. I used Chat GPT 4O to write this program for me. The present bugs are definitely thanks to Chat GPT's shortcomings. Although I do not like Eleven Labs anymore, I have no desire nor intention to continuously spam their servers until the script works properly if it ever does.

I'm hoping to get some actual developers to work on this and help me fix bugs. If you have the time, please consider submitting pull requests. I'd love to continue working on this program so that people have an easier time getting their data back, and I'm doing the best I can with the limited experience I have. But because of my limited experience, I cannot do this by myself. Your support would mean the world to me.