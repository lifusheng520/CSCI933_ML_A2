# ----------------------------------------------------------------------
# Config for data cleaning process
# ----------------------------------------------------------------------
# Speakers that should be removed entirely (exact match or substring)
INVALID_SPEAKERS = {
    "COMMERCIALLY",
    "WITH PERMISSION",
}

# Additional patterns that indicate a line is a copyright notice
COPYRIGHT_PATTERNS = [
    r"SHAKESPEARE IS COPYRIGHT 1990-1993 BY WORLD LIBRARY, INC., AND IS",
    r"WITH PERMISSION\.\s*ELECTRONIC AND MACHINE READABLE COPIES.*",
    r"PROHIBITED COMMERCIAL DISTRIBUTION.*",
    r"End of this Etext.*",
]

# List of Hamlet's updated scene summaries
IMPROVED_HAMLET_SUMMARIES = {
    "hamlet_1_1": "On the castle watch, Bernardo, Marcellus, and Horatio see a ghost that looks like the dead King Hamlet. Horatio connects the ghost to Denmark's fear of war with Fortinbras, and the guards decide to tell Prince Hamlet.",
    "hamlet_1_2": (
        "Claudius appears as the new King of Denmark after the death of Hamlet's father, King Hamlet, "
        "and his quick marriage to Queen Gertrude. Prince Hamlet is introduced as the grieving Prince of Denmark, "
        "the son of the dead King Hamlet and Gertrude, and the nephew and now stepson of Claudius. Hamlet is angry "
        "and heartbroken over his father's death and his mother's fast remarriage. At the end of the scene, Horatio "
        "tells Hamlet that a ghost resembling his dead father has appeared, beginning Hamlet's path toward discovering "
        "the truth and seeking revenge."
    ),
    "hamlet_1_3": "Laertes and Polonius warn Ophelia not to trust Hamlet's romantic attention because his royal position limits his freedom to choose. Ophelia agrees to obey her father, creating tension between love, family control, and politics.",
    "hamlet_1_4": (
        "Hamlet waits at night with Horatio and Marcellus to see the ghost of his father. When the ghost appears, "
        "Hamlet follows it even though his friends fear it may be dangerous or evil. This scene shows Hamlet's courage, "
        "grief, curiosity, and willingness to risk himself to learn the truth about his father's death."
    ),

    "hamlet_1_5": (
        "The ghost of the dead King Hamlet tells Prince Hamlet that Claudius murdered him by pouring poison in his ear "
        "while he slept. The ghost commands Hamlet to avenge the murder, making Hamlet responsible for punishing his "
        "father's killer. Hamlet is shocked by the truth, swears Horatio and Marcellus to secrecy, and accepts the burden "
        "of revenge against Claudius."
    ),
    "hamlet_2_1": "Polonius sends Reynaldo to spy on Laertes in Paris, showing Polonius's habit of controlling others. Ophelia then reports Hamlet's strange behaviour, and Polonius decides Hamlet must be mad because of rejected love.",
    "hamlet_2_2": (
        "Claudius and Gertrude ask Rosencrantz and Guildenstern to spy on Prince Hamlet because they are worried about "
        "his strange behaviour. Hamlet recognises that his old friends have been sent to observe him. When the travelling "
        "players arrive, Hamlet plans to stage a play that imitates his father's murder so he can test whether Claudius "
        "is guilty. This scene shows Hamlet investigating Claudius before taking revenge."
    ),
    "hamlet_3_1": "Claudius and Polonius secretly watch Hamlet speak with Ophelia. Hamlet reflects on life and death in the \"To be or not to be\" speech, rejects Ophelia harshly, and makes Claudius fear that his madness may be dangerous.",
    "hamlet_3_2": "Hamlet stages The Mousetrap, a play that mirrors King Hamlet's murder, to observe Claudius's reaction. Claudius interrupts the performance, convincing Hamlet that the ghost told the truth.",
    "hamlet_3_3": "Claudius privately admits his guilt and tries to pray, while Hamlet finds him alone and considers killing him. Hamlet delays because he does not want Claudius's soul to go to heaven, showing how revenge becomes morally complicated.",
    "hamlet_3_4": "Hamlet confronts Gertrude in her chamber and accidentally kills Polonius, who is hiding behind the curtain. The ghost reappears to remind Hamlet of his revenge, while Hamlet urges Gertrude to reject Claudius.",
    "hamlet_4_1": (
        "Gertrude tells Claudius that Hamlet has killed Polonius while confronting her in her chamber. Claudius becomes "
        "alarmed because Hamlet now seems dangerous and politically risky. He worries about blame, public order, and his "
        "own safety, so he decides Hamlet must be controlled and sent away."
    ),
    "hamlet_4_2": "Hamlet refuses to tell Rosencrantz and Guildenstern where he has hidden Polonius's body. His mocking answers show his distrust of them and his anger at being used by Claudius.",
   "hamlet_4_3": (
        "Claudius questions Hamlet about where he has hidden Polonius's body, while Hamlet answers with dark jokes about "
        "death and decay. Claudius decides to send Hamlet to England and secretly sends orders for Hamlet to be executed "
        "there. This scene shows Claudius turning his fear of Hamlet into a murder plot."
    ),

    "hamlet_4_4": (
        "Hamlet meets a captain from Fortinbras's army and learns that soldiers are risking their lives for a small and "
        "almost worthless piece of land. Their willingness to act makes Hamlet criticise his own delay in avenging his "
        "father. This scene renews Hamlet's resolve to take revenge against Claudius."
    ),
    "hamlet_4_5": "Ophelia appears mentally broken after Polonius's death, while Laertes returns angrily from France and threatens rebellion. Claudius tries to redirect Laertes's anger toward Hamlet.",
    "hamlet_4_6": "Horatio receives a letter from Hamlet explaining that pirates attacked his ship and returned him to Denmark. The letter reveals that Hamlet has escaped the journey to England and is coming back.",
    "hamlet_4_7": "Claudius and Laertes plan to kill Hamlet using a poisoned sword during a fencing match, with poisoned wine as a backup. Gertrude then reports that Ophelia has drowned, deepening Laertes's grief and anger.",
    "hamlet_5_1": (
        "In the graveyard, Hamlet reflects on death while watching gravediggers prepare Ophelia's grave. He holds Yorick's "
        "skull and thinks about how all people, even kings and jesters, end in death. When Ophelia's funeral arrives, "
        "Hamlet and Laertes clash over their grief for her."
    ),

    "hamlet_5_2": (
        "Hamlet explains how he escaped Claudius's plot to have him killed in England, then accepts the fencing match with "
        "Laertes. During the poisoned duel, Gertrude drinks poisoned wine, Laertes and Hamlet are wounded, and Hamlet kills "
        "Claudius after learning the truth. Hamlet dies, and Fortinbras arrives to take political control of Denmark."
    )
}

# List of Macbeth's updated scene summaries
IMPROVED_MACBETH_SUMMARIES = {
    "macbeth_1_1": "The three witches meet during thunder and lightning and plan to meet Macbeth after the battle. Their words, \"fair is foul, and foul is fair,\" introduce the play's dark mood, moral confusion, and connection between prophecy and Macbeth's future.",
    "macbeth_1_2": (
        "King Duncan hears reports that Macbeth and Banquo fought bravely and loyally against rebels and the Norwegian army. "
        "Macbeth is first presented as a heroic soldier who protects Scotland. Duncan rewards Macbeth with the title Thane of "
        "Cawdor, unknowingly preparing the first witches' prophecy to come true and setting up Macbeth's later temptation by power."
    ),

    "macbeth_1_3": (
        "The Three Witches's prophecy triger Macbeth's ambition, leading him to kill Duncan. "
        "Macbeth and Banquo meet the Three Witches, who greet Macbeth as Thane of "
        "Glamis, Thane of Cawdor, and future king. The prophecy unsettles Macbeth, "
        "especially when Ross arrives to confirm he is now Thane of Cawdor. "
        "Ambition begins to take root."
    ),

    "macbeth_1_4": (
        "King Duncan praises Macbeth for his bravery and loyalty, but then names Malcolm as heir to the throne. Macbeth realises that "
        "Malcolm now stands between him and the crown. This turns the witches' prophecy into a dangerous ambition because Macbeth sees "
        "that becoming king will not happen naturally. His private thoughts suggest that he is already considering dark action to gain power."
    ),
    "macbeth_1_5": 
        "Lady Macbeth persuade Macbeth to murder Duncan. "
        "Lady Macbeth reads Macbeth's letter about the prophecy and fears he is too "
        "kind to seize the crown. She calls on dark forces to harden her resolve "
        "and urges Macbeth to kill Duncan when he arrives at their castle.",
    "macbeth_1_6": "Duncan arrives at Macbeth's castle and praises its pleasant appearance, unaware that Macbeth and Lady Macbeth are planning his murder. The scene creates dramatic irony because the king trusts the people who are about to betray him.",
    "macbeth_1_7": (
        "Macbeth debates whether to murder Duncan and lists strong reasons not to do it: Duncan is his king, his guest, his relative, "
        "and a good ruler. Macbeth admits that his only real motive is vaulting ambition. Lady Macbeth attacks his courage and masculinity, "
        "persuading him to continue with the murder plan. This is the clearest evidence scene for why Macbeth kills Duncan: ambition, "
        "desire for the crown, and Lady Macbeth's pressure overcome his conscience."
    ),

    "macbeth_2_1": (
        "Banquo is uneasy about the witches' prophecy, while Macbeth prepares to murder Duncan. Macbeth sees an imaginary dagger leading "
        "him toward Duncan's room, revealing his fear, guilt, and violent ambition before the murder. This scene shows Macbeth crossing "
        "from thought into action as he moves toward killing Duncan for the crown."
    ),
    "macbeth_2_2": "Macbeth murders Duncan and returns shaken, carrying the bloody daggers. Lady Macbeth tries to stay calm and returns the daggers herself, but Macbeth's guilt and horror show that the murder has deeply disturbed him.",
    "macbeth_2_3": (
        "Macduff discovers Duncan's murdered body, and Macbeth kills Duncan's guards before they can speak. Macbeth claims he killed them "
        "out of loyal rage, but this also helps cover his own crime. Malcolm and Donalbain flee because they fear they may be killed next, "
        "which clears Macbeth's path to the throne. This scene is useful evidence for the aftermath of Duncan's murder, while Macbeth's "
        "motivation is better shown in Acts 1.3, 1.4, 1.5, 1.7, and 2.1."
    ),
    "macbeth_2_4": "Ross and an old man discuss strange events in nature after Duncan's murder, suggesting that Scotland itself is disturbed. Macduff reports that Macbeth has been named king, while suspicion remains around Malcolm and Donalbain.",
    "macbeth_3_1": "Macbeth feels unsafe as king because Banquo heard the witches' prophecy and Banquo's descendants are predicted to inherit the throne. Macbeth secretly hires murderers to kill Banquo and Fleance, showing that his ambition has turned into paranoia and tyranny.",
    "macbeth_3_2": "Macbeth and Lady Macbeth admit that gaining the crown has not brought peace or happiness. Macbeth hides his plan to kill Banquo and Fleance from Lady Macbeth, showing that he is becoming more independent, secretive, and ruthless.",
    "macbeth_3_3": "The murderers attack Banquo and Fleance on the road. Banquo is killed, but Fleance escapes, meaning the prophecy about Banquo's descendants remains a threat to Macbeth.",
    "macbeth_3_4": "At the royal banquet, Macbeth sees Banquo's ghost and reacts with terror in front of the nobles. Lady Macbeth tries to cover for him, but Macbeth's guilt and instability become publicly visible.",
    "macbeth_3_5": (
        "Hecate criticises the witches for dealing with Macbeth without her and plans to mislead him with false confidence. This scene prepares "
        "the later apparitions that will make Macbeth feel safe even while they lead him toward destruction."
    ),
    "macbeth_3_6": "Lennox and another lord discuss Macbeth's growing tyranny and suspect him of Duncan and Banquo's murders. They reveal that Macduff has gone to England to support Malcolm and seek help against Macbeth.",
    "macbeth_4_1": "The witches show Macbeth apparitions that warn him about Macduff, claim that no man born of woman can harm him, and say he is safe until Birnam Wood comes to Dunsinane. Macbeth becomes overconfident but decides to kill Macduff's family.",
    "macbeth_4_2": "Lady Macduff feels abandoned because Macduff has fled to England, and she tries to explain his absence to their son. Macbeth's murderers arrive and kill Macduff's family, showing the cruelty of Macbeth's rule.",
    "macbeth_4_3": "In England, Malcolm tests Macduff's loyalty before trusting him. Ross then reveals that Macbeth has murdered Macduff's wife and children, and Macduff turns his grief into a promise of revenge.",
    "macbeth_5_1": (
        "Lady Macbeth sleepwalks and tries to wash imaginary blood from her hands, crying out about the guilt she cannot remove. Her words reveal "
        "her hidden guilt over Duncan, Banquo, and Lady Macduff. This scene shows that the crimes she once encouraged have destroyed her mind."
    ),
    "macbeth_5_2": "Scottish nobles gather near Birnam Wood to join Malcolm's army against Macbeth. They describe Macbeth as a tyrant whose soldiers obey from fear, not loyalty.",
    "macbeth_5_3": (
        "Macbeth clings to the witches' prophecies and believes he cannot be defeated, even as enemies approach and his supporters desert him. "
        "His confidence comes from misunderstanding the apparitions' double meanings. He also hears that Lady Macbeth is ill, showing the collapse "
        "of both his rule and his household."
    ),
    "macbeth_5_4": "Malcolm orders each soldier to cut a branch from Birnam Wood and carry it as camouflage while marching toward Dunsinane. This military strategy unknowingly begins to fulfil the witches' prophecy.",
    "macbeth_5_5": "Macbeth learns that Lady Macbeth has died and responds with despair about the meaninglessness of life. A messenger then reports that Birnam Wood appears to be moving toward Dunsinane, shaking Macbeth's confidence in the prophecy.",
    "macbeth_5_6": "Malcolm's army reaches Dunsinane, throws down the branches used as camouflage, and begins the assault. The prophecy about Birnam Wood has now come true in a practical military way.",
    "macbeth_5_7": (
        "Macbeth fights desperately outside the castle, still trusting the prophecy that no one born of woman can kill him. He kills young Siward, "
        "but his confidence depends on a misleading interpretation of the witches' words. Meanwhile, Macduff searches for Macbeth to avenge his "
        "murdered family."
    ),
    "macbeth_5_8": "Macduff confronts Macbeth and reveals that he was born by caesarean section, not by ordinary birth. Macbeth realises the witches misled him with double meanings, but he fights on and is killed by Macduff.",
    "macbeth_5_9": "Macduff enters with Macbeth's severed head, proving that the tyrant is dead. Malcolm becomes king, rewards his supporters, and promises to restore order to Scotland after Macbeth's violent rule."
}

# List of Romeo and Juliet's updated scene summaries
IMPROVED_ROMEO_AND_JULIET_SUMMARIES = {
    "romeo_and_juliet_0_0": (
        "The Chorus introduces the ancient feud between the Montagues and Capulets in Verona. The prologue explains that Romeo "
        "and Juliet are star-crossed lovers from enemy families, and that their deaths will finally end their parents' hatred. "
        "This scene is key evidence for questions about the Montague-Capulet conflict, the family feud, fate, and the tragic love story."
    ),

    "romeo_and_juliet_1_1": (
        "A public fight breaks out between Capulet and Montague servants, showing that the family feud affects not only the nobles "
        "but also their households and servants. Old Capulet and Old Montague also try to join the violence, proving that the hatred "
        "is long-standing and deeply rooted. Prince Escalus stops the fight and warns both families that further violence will be punished. "
        "Romeo then appears lovesick because Rosaline does not return his love."
    ),
    "romeo_and_juliet_1_2": "Paris asks Capulet for permission to marry Juliet, but Capulet says Juliet is still young and should decide for herself. Romeo and Benvolio learn about the Capulet feast, giving Romeo the chance to meet Juliet.",
    "romeo_and_juliet_1_3": "Lady Capulet and the Nurse talk to Juliet about Paris as a possible husband. Juliet agrees to look at Paris during the feast, introducing the pressure on her to marry according to her family's wishes.",
    "romeo_and_juliet_1_4": "Romeo, Mercutio, and Benvolio prepare to attend the Capulet feast in disguise. Mercutio mocks dreams with his Queen Mab speech, while Romeo fears that going to the party may begin a tragic chain of events.",
     "romeo_and_juliet_1_5": (
        "Romeo and Juliet meet at the Capulet feast and instantly fall in love before knowing each other's family identity. After Romeo "
        "learns that Juliet is a Capulet, he realises his life is tied to his enemy. Juliet then learns from the Nurse that Romeo is a "
        "Montague, the only son of her family's great enemy. Juliet is conflicted because she is a Capulet who loves Romeo, a Montague. "
        "Her line 'My only love sprung from my only hate' shows the central conflict between romantic love and the Montague-Capulet feud."
    ),

    "romeo_and_juliet_2_0": (
        "The Chorus explains that Romeo's old love for Rosaline has been replaced by his new love for Juliet, and that Juliet loves Romeo too. "
        "However, their love is dangerous because Romeo is a Montague and Juliet is a Capulet, meaning they belong to enemy families. This scene "
        "summarises their conflict after meeting: they love each other, but the feud makes it difficult for them to meet, speak, or love openly."
    ),
    "romeo_and_juliet_2_1": "After leaving the feast, Romeo hides from Mercutio and Benvolio instead of going home. His friends joke about Rosaline, not realising that Romeo has forgotten her and is now seeking Juliet.",
    "romeo_and_juliet_2_2": "In the balcony scene, Romeo overhears Juliet confess her love for him. They declare their love despite the danger of their family names and agree to arrange a secret marriage.",
    "romeo_and_juliet_2_3": "Romeo asks Friar Laurence to marry him and Juliet. Although surprised by Romeo's sudden change from Rosaline to Juliet, Friar Laurence agrees because he hopes the marriage may end the feud between the families.",
    "romeo_and_juliet_2_4": "Mercutio and Benvolio joke with Romeo before the Nurse arrives to receive Romeo's marriage message. Romeo tells the Nurse that Juliet should come to Friar Laurence's cell, making the Nurse an important helper in the secret plan.",
    "romeo_and_juliet_2_5": "Juliet anxiously waits for the Nurse to return with Romeo's message. The Nurse delays the news, increasing Juliet's frustration, before finally telling her to go to Friar Laurence for the secret wedding.",
    "romeo_and_juliet_2_6": "Romeo and Juliet meet Friar Laurence and prepare to marry in secret. The scene shows their intense love and hope, while Friar Laurence warns that sudden, extreme passion can end badly.",
     "romeo_and_juliet_3_1": (
        "Tybalt challenges Romeo, but Romeo refuses to fight because he has secretly married Juliet and now sees Tybalt as family. Mercutio fights "
        "Tybalt instead and is killed. In anger and revenge, Romeo kills Tybalt. Prince Escalus banishes Romeo from Verona, turning the private love "
        "between Romeo and Juliet into a public crisis. This scene is the major turning point of the tragedy."
    ),
    "romeo_and_juliet_3_2": "Juliet waits for Romeo after their secret marriage, but the Nurse brings news that Romeo has killed Tybalt and been banished. Juliet struggles between grief for Tybalt, love for Romeo, and fear that their marriage is already falling apart.",
    "romeo_and_juliet_3_3": (
        "Romeo hides in Friar Laurence's cell after being banished for killing Tybalt. He reacts desperately and sees banishment from Verona and Juliet "
        "as worse than death. Friar Laurence tells him to spend the night with Juliet, then flee to Mantua until the families can be reconciled."
    ),
    "romeo_and_juliet_3_4": "Capulet decides that Juliet will marry Paris very soon, believing the wedding will help her recover from Tybalt's death. This creates a crisis because Juliet is already secretly married to Romeo.",
    "romeo_and_juliet_3_5": "Romeo and Juliet say goodbye after their wedding night because Romeo must leave for Mantua. Juliet's parents then order her to marry Paris, and when she refuses, Capulet threatens to reject her, leaving Juliet isolated and desperate.",
    "romeo_and_juliet_4_1": "Paris discusses his wedding plans with Friar Laurence, while Juliet arrives in distress. Friar Laurence gives Juliet a potion that will make her appear dead so she can avoid marrying Paris and reunite with Romeo.",
    "romeo_and_juliet_4_2": (
        "Juliet returns home and pretends to obey her father by agreeing to marry Paris, even though she is already secretly married to Romeo. Capulet "
        "is pleased and moves the wedding earlier, which increases the danger because Juliet must take Friar Laurence's potion sooner than planned."
    ),
    "romeo_and_juliet_4_3": "Alone in her room, Juliet fears the potion may fail, kill her, or leave her trapped in the tomb. Despite her terror, she drinks it because she sees no other way to stay faithful to Romeo.",
    "romeo_and_juliet_4_4": "The Capulet household busily prepares for Juliet's wedding to Paris. The cheerful preparations create dramatic irony because Juliet has already taken the potion and appears to be dead.",
    "romeo_and_juliet_4_5": "The Nurse discovers Juliet apparently dead, and the Capulet household turns from wedding celebration to mourning. Friar Laurence tells the family to prepare Juliet for burial, allowing his secret plan to continue.",
    "romeo_and_juliet_5_1": (
        "In Mantua, Romeo hears from Balthasar that Juliet is dead, not knowing her death is fake. Because Friar Laurence's message has not reached him, "
        "Romeo believes the false news and decides to die beside Juliet. He buys poison, turning misinformation into the immediate cause of his fatal decision."
    ),

    "romeo_and_juliet_5_2": (
        "Friar John tells Friar Laurence that he could not deliver the letter explaining Juliet's fake death to Romeo. Friar Laurence realises that Romeo "
        "does not know the plan and that Juliet may wake alone in the tomb. This failed message is a major cause of the final tragedy."
    ),

    "romeo_and_juliet_5_3": (
        "At Juliet's tomb, Romeo kills Paris, then drinks poison because he believes Juliet is truly dead. Juliet wakes and finds Romeo dead, then kills "
        "herself with his dagger. The deaths of Romeo and Juliet finally force the Montagues and Capulets to recognise the damage caused by their feud, "
        "and the grieving families agree to end their hatred."
    )
}