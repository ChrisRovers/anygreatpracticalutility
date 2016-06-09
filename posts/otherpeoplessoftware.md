date = 2016-05-09
title = Other People's Software
tags = philosophy programming
+++

This post is about none of the things on my post list from the 'beginnings' post,
but it interested me, so I'm writing about it anyways.

The thing that struck me as I went through the motions of figuring out a place to
put this blog, figuring out what technology to use to produce it and so on is just
how much software we all need to learn, day in and day out.  At work, it is just
kind of expected, so you don't necessarily put it all together, but we do end up
learning a ridiculous amount.  Over the last week, for specific work issues, I learned :

* more about Angular2's routing, default routes and async routes
* a new version of nmap and its windows wrapper/launcher
* fuzzing in ZAP Attack Proxy
* Burp Suite's insane UI
* the zxcvbn password entropy calculation library (and its Java port)
* nginx configuration and CORS handling

There's probably stuff there that I've forgotten I had to deal with, too.  The thing is, 
none of those pieces of software are that difficult, but each has its own cost. I don't
mean dollars - though Burp Suite is paid software, the rest of them are not - but mental
cost.  Everytime you learn a piece of technology, you end up having to squish the way
you think about the topic into the way the program author(s) thought about it. Sometimes, there's
a pretty good match.  And sometimes (like with me and Burp Suite's UI), there just isn't. But
that's the way it goes - when you are working on a piece of 'enterprise' software and the
deadlines are coming fast, you do things the sensible way, by avoiding the 'not invented here syndrome' and by
'not inventing the wheel.' 

And that might make sense in a situation where other people need to be able to use the stuff
you built, where you don't have time to fully document a customization or a custom piece of
software.. but it was lovely and freeing to realize it really didn't make any sense in the context 
of this blog.

I had decided early on that I wanted to use static html generation as the basic technology
behind the blog, coupled with something like Disqus to handle comments where I wanted them.  So I started
poking around at static website generators - Hugo, Jekyll, Hyde, some others.  None of them were
bad at all, but everytime I started down a path to make a website with one, I just.. petered off.  There was
that mental cost of absorbing the docs and none of them quite fit they way I considered the situation, and without
the driving need of a paying job, it caused me to keep punting on creating the website.  That effort of 
cramming my brain into someone else's paradigm just wasn't worth it. 

That's why it was such a relief to realize I didn't need to care about anyone maintaining this
thing other than me.  I had to be reasonably kind to my future self, but he was the only
consumer of the infrastructure side.  And future me, well, he probably can manage to cram
his brain into the way current me thinks.  And that meant that I could just write my
own generator.  It doesn't take much to do a static website generator - if you are reading this, 
it means that I have finished, after all.  At the time of this writing, it is pretty much done,
except for adding Disqus support, and is less than 180 lines of Python.  And it was so much
MORE FUN to do it this way.  From a mental cost perspective, it was better than free - it
was enjoyable.

It isn't the most full featured generator in the world - it is designed to generate this website.
It uses templates, of course, since I wanted to be able to edit the HTML reasonably (and I started 
with a Creative Commons css/html template), and nobody likes writing HTML in print statements.  
But it makes lots of assumptions that Hugo and its ilk cannot - and that means that it is 
far, far simpler.  Cheap to think about.  I doubt I'll release it - just because
it is cheap for me, doesn't mean it'll be cheap for you.  But that's kind of the point - when possible,
when you can, consider the mental cost of different paths and take the lovely, fun, free path that goes
*your own way*. 

-cdr