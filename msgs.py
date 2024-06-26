from numerize import numerize 

failedToScan="Failed to scan your link! This may be due to an incorrect link, private/suspended account, deleted tweet, or recent changes to Twitter's API (Thanks, Elon!)."
failedToScanExtra = "\n\nTwitter gave me this error: "
tweetNotFound="Tweet not found."
unknownError="Unknown Error"
tweetSuspended="This Tweet is from a suspended account." 

videoDescLimit=220
tweetDescLimit=340

def genLikesDisplay(vnf):
    if vnf['retweets'] > 0:
        return ("\n\n💖 " + numerize.numerize(vnf['likes']) + " 🔁 " + numerize.numerize(vnf['retweets']))
    else:
        return ("\n\n💖 " + numerize.numerize(vnf['likes']))

def genQrtDisplay(qrt):
    verifiedCheck = "☑️" if ('verified' in qrt and qrt['verified']) else ""
    return ("\n\n【QRT of " + qrt['user_name'] + " (@" + qrt['user_screen_name'] + ")"+ verifiedCheck+":】\n'" + qrt['text'] + "'")

def genPollDisplay(poll):
    pctSplit=10
    output="\n\n"
    for choice in poll["options"]:
        output+=choice["name"]+"\n"+("█"*int(choice["percent"]/pctSplit)) +" "+str(choice["percent"])+"%\n"
    return output

def formatEmbedDesc(type,body,qrt,pollData,likesDisplay):
    # Trim the embed description to 248 characters, prioritizing poll and likes

    qrtType=None
    if qrt!=None:
        qrtType="Text"

    limit = videoDescLimit if type=="Text" or type=="Video" or (qrt!=None and (qrtType=="Text" or qrtType=="Video")) else tweetDescLimit

    output = ""
    if pollData==None:
        pollDisplay=""
    else:
        pollDisplay=genPollDisplay(pollData)

    if qrt!=None:

        qrtDisplay=genQrtDisplay(qrt)
        if 'id' in qrt and ('https://twitter.com/'+qrt['screen_name']+'/status/'+qrt['id']) in body:
            body = body.replace(('https://twitter.com/'+qrt['screen_name']+'/status/'+qrt['id']),"")
            body = body.strip()
        body+=qrtDisplay
        qrt=None

    if type=="" or type=="Video":
        output = body+pollDisplay+likesDisplay
    elif qrt==None:
        output= body+pollDisplay+likesDisplay
    else:
        output= body + likesDisplay
    if len(output)>limit:
        # find out how many characters we need to remove
        diff = len(output)-limit
        # remove the characters from body, add ellipsis
        body = body[:-(diff+1)]+"…"
        return formatEmbedDesc(type,body,qrt,pollData,likesDisplay)
    else:
        return output
