import random

def getResponse(list: list) -> str:
    return random.choice(list)

CheckFailure = [
    "A.C.C.E.S.S  D.E.N.I.E.D", 
    #"No, kys <3", 
    "Pah, come back when you're atleast some level of staff.", 
    "No Perms, [L](https://images-ext-2.discordapp.net/external/rdIZ3gPbAPNV2Yx26E_qnn2j7ythQf6vARC6Ggsmzbg/https/cdn.discordapp.com/emojis/802045878700736553.png?format=webp&quality=lossless&width=80&height=80)", 
    "You can run this command *after* I get a pay raise, mmm?", 
    "Yeah, nah. You're missing perms.", 
    "Aye aye, calm down, you're not allowed to do this.", "Why're you trying to use commands outside of your own power, *friend*?"
    ]

Blacklisted = [
    "It seems you've been blacklisted... from the entire bot. Congrats!",
    "Sigh, you've been blacklisted. Stop trying to run my commands, please.",
    "Blacklisted user detected, request rejected."
]

NotFound = [
    "Couldn't find that command",
    "That command doesn't exist ;-;",
    "Check the help page before trying to get me to do something that doesn't exist",
    "You probably forgot how to spell, because that command doesn't exist.",
    "I dunno what you're asking of me ;-;",
    "That command doesn't exist :c"
]

MissingArg = [
    "You're missing an arguement!",
    "You haven't given me enough information to execute this command :(",
    "Please input all required arguments, thanks."
]

Cooldown = [
    "Hey, hold your horses there buckaroo. Command's on cooldown.",
    "Command on Cooldown.",
    "You're not ready enough to run this command, gotta wait for it to cool down."
]

BadArgument = [
    "You inputted a bad arguement, try again.",
    "I failed to understand one of your arguments, use ``>>help (cmd name)`` to check them.",
    "I sure hope this is a joke... I really don't want to presume you can't read.",
    "Invalid input, try again.",
    "Hey, at least you *put in* a value... even if it is horridly wrong."
]


Disabled = [
    "This command is disabled.",
    "Command out of order",
    "This command is either WIP, Obsolete, or something Nexus forgot about"
]


shouldI = [
    # Neutral/General
    "Yes, you should! It seems like a great idea.",
    "Nah, not feeling like that's a good option.",
    "I highly endorse that choice!",
    "Hmm, I'm not so sure about that. Perhaps reconsider?",
    "Absolutely, go for it!",
    "I'd advise against it, based on what I know.",
    "That sounds fantastic! Why not?",
    "Maybe not the best idea. Have you thought about the consequences?",
    "Certainly! That sounds very promising.",
    "I'm inclined to say no, it doesn't seem like the best move.",
    "It's a yes from me. Sounds like you've thought it through.",
    "I'm hesitant to say yes. Maybe gather more information first?",
    "Definitely a good choice, in my opinion.",
    "That might not be the wisest decision. Maybe explore other options?",
    "Sure thing, it seems like a safe and sound decision.",
    "I'd be cautious about that. It might not turn out as expected.",
    "It looks like a solid plan. I say go for it.",
    "It's a no from me. It seems a bit risky, don't you think?",
    "I support that decision. It seems well thought out.",
    "I wouldn't recommend it. It doesn't seem like the best course of action.",

    # Satirical
    "Oh, absolutely. Because that's exactly what the world needs right now.",
    "Sure, join the club. Everyone's doing it, even those with common sense.",
    "Of course, because every great story starts with a 'Hold my beer' moment.",
    "Why not? After all, good decisions make stories, bad ones make legends.",
    "Yes, do it! The world is your oyster... or at least, the comedic relief.",

    # Sadistic
    "Yes, the path to misery awaits you with open arms.",
    "Sure, go ahead. I enjoy watching train wrecks in slow motion.",
    "Oh, definitely. It's not a true disaster until you join in.",
    "Absolutely, chaos is a ladder and you seem ready to fall off it.",
    "Sure, why not? I've always wondered what a real-life facepalm looks like.",

    # Tsundere
    "It's not like I care what you do, but... maybe it's not a terrible idea.",
    "Hmph. Do whatever you want, not like it matters to me... though it might actually be good.",
    "I guess you can, but don't misunderstand, it's not like I approve or anything!",
    "Sure, go ahead. Not that I’ll be watching or anything, b-baka!",
    "Maybe you should, maybe you shouldn’t. What do I care? But, well, it might be okay…",

    # Bland
    "If you want to, I guess. I don't have a strong opinion.",
    "Sure, do it or don't. It's all the same to me.",
    "Okay, sounds like an activity that exists.",
    "Might as well. Not that it makes any difference.",
    "Go for it, or not. I don’t really mind either way.",

    # Bored
    "Yeah, whatever. It's not like there's anything better to do.",
    "Go ahead, not like it's going to make my day any more interesting.",
    "Sure, might as well. It's not like I have anything more exciting going on.",
    "Do it, don’t do it – I couldn’t be less interested.",
    "Yeah, go on. Maybe it'll give me something to be less bored about.",

    # Funny
    "Sure, why not? I mean, what's the worst that could happen? ||(Famous last words.)||",
    "Yes, and if you need an alibi, I was with you the whole time.",
    "Yes, and if it doesn't work out, we can always say it was a social experiment.",
    "Go for it! Life's too short to not do weird stuff.",
    "Go for it! I'll be here, snacking on popcorn and watching the chaos unfold.",
    "If you do it, it'll be the second funniest thing I've seen. First is my reflection.",
    "Absolutely! Remember, 'Yolo' is just 'Carpe Diem' for lazy people.",
    "Definitely! I mean, if we're not here for a laugh, then what are we here for?",
    "Sure! And if anyone asks, we'll say it was my idea.",
    "Absolutely! Let's add a bit of sparkle to this otherwise mundane existence.",


    # Laid-back (Chill)
    "Yeah, why not? Take it easy and see how it goes~",
    "Sure thing, just roll with it and enjoy the ride~",
    "Go for it, no pressure~\nWhat's life without a little adventure~?",
    "Definitely, just keep it cool and relaxed~~",
    "Yeah, sounds good. Keep it chill and everything will be fine~",

    # Positive
    "Absolutely, I believe in you! Go make it happen!!",
    "Yes, you've got this! I'm rooting for you all the way!!!",
    "Certainly! Your enthusiasm is contagious, let's do this!",
    "Of course! I have every confidence in your success!~",
    "Yes, your positivity is inspiring! Go for it with all you've got~",

    # Ren
    "I disagree with this decision because it fails to account for various factors such as differing opinions, perspectives, and experiences. While some people may believe that teachers are important, it is also important to consider the various perspectives and backgrounds of individuals and to approach disagreements with an open mind and a willingness to explore various viewpoints. It is essential to remember that not everyone will share the same opinion, and respecting different perspectives is integral to fostering a healthy and inclusive learning environment",
    "Ren proves that your statement is invalid, and this choice could not possibly be any worse."
]
