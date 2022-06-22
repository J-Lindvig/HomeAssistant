# Publish to HACS
So you have created a fancy integration for Home Assistant, congratulations, and now wish to share it with the world using HACS.This guide will assist you in your journey.

## Disclaimer
I am not an affiliate of HACS or Home Assistant and my guide is simply how I do it.Perhaps this is not the best or the most appropriate way.It is, however, the results of my trial/ error, due to the lack of (IMHO) an easyunderstandable documentation. If in doubt, please refer to the official [documentation](https://hacs.xyz/docs/publish/start).

## General requirements

### Github account
You **must** have a Github account, which you likely already have, if not please start with a [signup](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home).

### Public repository
Create a repository new **public** repository in Github account.
Adding a **License** is optional but recommended. For help in choosing the right license, I refer to [choosealicense.com](https://choosealicense.com/)

### Description and Topics
In the frontpage of your newly created repository, click *About* and fill in:
1. Description
2. Topics
<figure>
    <img src="https://user-images.githubusercontent.com/54498188/175000987-0c68fe88-ef07-45a1-9c26-bf1cfbd0188e.png"
         alt="Dialogbox with description and topics">
    <figcaption>Description and topics from my Flagdays_DK integration.</figcaption>
</figure>

### readme.md
It is required for your repository to have a readme.md containing information on how to install, config and use the integration.
Help in formatting the readme.md can be found in this [cheatsheet](https://www.markdownguide.org/cheat-sheet/).
The file is **only** used in HACS
