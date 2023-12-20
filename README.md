
---
# ***Thuisweb***

1. [Summary](#summary)
2. [How's progress?](#hows-progress)
    * [Technical](#technical)
    * [Functionality](#functionality)
3. [Current pages](#current-pagesroutes)
4. [How to install?](#how-to-install)
5. [How to un-install?](#how-to-un-install)
6. [If something is missing](#if-something-is-wrong-or-missing)


## *Summary*

&nbsp;&nbsp;&nbsp;&nbsp;This is ***the*** website for your home network. im following a tutorial on youtube called Flask Friday with John Elder at 
codemy.com. (yes the guy looks a lot like the guy from breaking bad). Nonetheless I had to improvise since John doesn't host the website from a docker server/container. ***I do!***
<br><br><br>

# *So, how's progress?*

## *Technical:*

&nbsp;&nbsp;&nbsp;&nbsp;I'm progressing quite good. As far as Technical progress is concerned: I think I'm done. The website runs on a docker container. Maybe a database gets added later on in the course but, thats as simple as copy and paste.

- App runs in a docker container.
- MySQL db runs 1 database `Gebruikers` with these tables: `gebruikers` and `posts` in a docker container.
- Both containers are connected.

## *Functionality:*

&nbsp;&nbsp;&nbsp;&nbsp;I am adding, Functionality wise, more and more each episode. It's a bit chaotic so to speak. I already know what I want to delete because of what I want from the website but I don't know if John uses it in a later episode. So I will add everything like John does with his course. And in the end I'll delete the stuff I dont need and try to add stuff i would like to add. 

### *Userwise you have:*
- The possibilty to create a profile with password.
- Edit the profile.
- Delete the profile.
- A table where you can see the other user accounts.


### *Blogwise you can:*
- Leave a blog- sort of - post.
- Read the blog posts posted on the website on a dedicated page.
- Open a singe blog post on its own page and go back to the blog-list thing. 

<br><br><br>

# *How to install??*
&nbsp;&nbsp;&nbsp;&nbsp;The only thing you'll need is `Git` and `Docker`. Those apps will install a clean version of the app in 4 simple steps once those apps are installed. K.K.D.W.D.[^1]
<br>
<br>

1. install by typing in terminal: [^2]
```bash
git clone https://github.com/BargeCode/Thuisweb.git
```
2. `cd` into folder
3. Let Docker compose:
```bash
 docker compose up -d
 ```
4. Open this webpage in your internet explorer when command line says [2/2] are running:
   [Thuisweb Homepage](localhost:3000/index.html) and take a look around!

# *How to Un-install??*

&nbsp;&nbsp;&nbsp;&nbsp;That's more difficult then installing.
1. First shutdown the entire docker stack and delete the created volume by typing in the CLI inside the folder where you `git cloned` this repository: 
```bash
docker compose down --volumes
```
2. Remove docker images through:
```bash
docker image rmi thuisweb-app mysql
```
3. delete the folder.

# *If something is wrong or missing.*

&nbsp;&nbsp;&nbsp;&nbsp;Please feel free to open an issue ticket. I will look into it and ofcourse... try to fix it. 

[^1]: K.K.D.W.D. is a dutch abbreviation for a saying. The saying: *"Kind Kan De Was Doen"* translated to English means: *"Child can do the laundry"*. Probably makes no sense but it means that its so easy, a child can do it. 
[^2]: Works on Mac and Linux.
