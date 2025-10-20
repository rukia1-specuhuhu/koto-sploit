"""Collection of ASCII cat art for Kotosploit"""

import random

CATS = [
    """
    /\_/\\  
   ( o.o ) 
    > ^ <
       """,
    """
   /\     /\\
  {  `---'  }
  {  O   O  }
  ~~>  V  <~~
   \  \|/  /
    `-----'
        """,
    """
    /\_/\\  
   ( o.o ) 
    > ^ <
   /     \\
  /       \\
 /         \\
        """,
    """
      /\\_/\\  
     ( o.o ) 
      > ^ <
     /     \\
    /       \\
   /         \\
  /           \\
        """,
    """
   |\      _,,,--,,_
   /,`.-'`'   ._  \-;;,_
  |,4-  ) )-,_..;\ (  `'-'
 '---''(_/--'  `-'\_)   )
        """,
    """
    /\_/\  
   ( o.o ) 
    > ^ <
    /|   |\\
   / |___| \\
        """
]

HACKER_CATS = [
    """
    (\__/)  ___
    (o^.^) |___|
    z(_(")(")  Hacking...
        """,
    """
     /\_/\     
    ( @.@ )  < Pentesting Mode
     > - <    
    /|   |\    
   (_|   |_)   
        """,
    """
    |\---/|
    | o_o |  << Exploiting...
     \_^_/
        """,
    """
    /\___/\
   (  ^w^  )  Security Cat
   (   =   )  is watching
    \  ~  /
        """,
    """
    /\_/\\  
   ( 0.0 ) 
   / >👾< \\
  /_______\\
        """,
    """
    /\_/\\  
   ( ^.^ ) 
   / >💻< \\
  /_______\\
        """,
    """
    /\_/\\  
   ( -.- ) 
   / >🔍< \\
  /_______\\
        """,
    """
    /\_/\\  
   ( o.o ) 
   / >⚡< \\
  /_______\\
        """,
    """
    /\_/\\  
   ( @.@ ) 
   / >🕵️< \\
  /_______\\
        """,
    """
    /\_/\\  
   ( *.* ) 
   / >🔓< \\
  /_______\\
        """
]

SPECIAL_CATS = [
    """
    /\_/\\  
   ( >^.^< ) 
   /  |  \\
  /___|___\\
     |   |
    /|___|\\
        """,
    """
   |\      _,,,--,,_
   /,`.-'`'   ._  \-;;,_
  |,4-  ) )-,_..;\ (  `'-')
 '---''(_/--'  `-'\_)   )
        """,
    """
    .--.           .--.
   /.._\\         /.._\\
   \\   \\.--.   .--./   //
    \\    \\..`-'.-'/    //
     \\    \\   '   /    //
      \\    \\     /    //
       \\    \\    /    //
        \\    \\   /    //
         \\    \\  /    //
          \\    \\ /    //
           \\    \\/    //
            \\          //
             \\        //
              \\      //
               \\    //
                \\/
        """,
    """
     A_A
    (-.-)
     |-|  
    /   \
   |     |   _
   |  || |  | |
  /_||||  |_/ /
    """,
    """
       |\___/|
       )     (
      =\     /=
        )===(
       /     \
       |     |
      /       \
     """,
    """
    /\___/\
   (  o o  )
   (  =^=  ) 
    )     (
   (       )
  (  (   (  )
 (__(__)___)
    """,
    """
       /\__/\
      /`    '\
     === 0  0 ===
       \  --  /
      /        \
     /          \
    |            |
    \  ||  ||  /
     \_oo__oo_/#######o
        """,
    """
     .       .
     |\_---/|
    /   o_o   \
   |  \     /  |
   / '  \_/  ' \
  / .'"     "'. \
        """
]

SLEEPING_CATS = [
    """
    |\      _,,,---,,_
    /,`.-'`'   -.  ;-;;,_
   |,4-  ) )-,_..;\ (  `'-'
  '---''(_/--'  `-'\_)   )
    Zzzz...
        """,
    """
    |\---/|
    | zzz |
     \_-_/
      | |
    """,
    """
    /\_/\\  
   ( -.-) 
    > - <
   /     \\
  /       \\
     Zzz
        """,
    """
     .-. .-.
    ( ( ( )
    ) ) )
    ( ( ( )
     '-.-'
      Zzz
        """
]

PLAYFUL_CATS = [
    """
    /\_/\\  
   ( ^.^ ) 
   / > ^ <\\
  /  | |  \\
 /___| |__\\
        """,
    """
     /\_/\  
    ( o.o ) 
    >  ^  <
   /  / \\ \\
  /  /   \\ \\
 /  /     \\ \\
        """,
    """
    /\_/\\  
   ( o.o ) 
    >  ^  <
   /  | |  \\
  /  /   \\ \\
 /  /     \\ \\
        """,
    """
    /\_/\\  
   ( o.o ) 
    >  ^  <
   /  / \\ \\
  /  /   \\ \\
 /  /     \\ \\
        """
]

HALLOWEEN_CATS = [
    """
    /\_/\\  
   ( ^.^ ) 
   > ^.^ <
   /  | |  \\
  /  /   \\ \\
 /  /     \\ \\
    👻
        """,
    """
    /\_/\\  
   ( o.o ) 
   > ^.^ <
   /  / \\ \\
  /  /   \\ \\
 /  /     \\ \\
    🎃
        """,
    """
    /\_/\\  
   ( ^.^ ) 
   > ^.^ <
   /  / \\ \\
  /  /   \\ \\
 /  /     \\ \\
    🦇
        """
]

CYBERPUNK_CATS = [
    """
    |\---/|
    | o_o |  << NEON CAT >>
     \_^_/
     /|   |\\
    / |___| \\
        """,
    """
    /\___/\
   (  ^w^  )  CYBERPUNK
   (   =   )  SECURITY CAT
    \  ~  /
     /|   |\\
    / |___| \\
        """,
    """
    /\_/\\  
   ( @.@ ) 
   / >🕵️< \\
  /_______\\
   | NEON |
        """,
    """
    /\_/\\  
   ( *.* ) 
   / >🔓< \\
  /_______\\
   | 2077 |
        """
]

CHRISTMAS_CATS = [
    """
    /\_/\\  
   ( ^.^ ) 
   > ^.^ <
   /  * *  \\
  /  /   \\ \\
 /  /     \\ \\
    🎄
        """,
    """
    /\_/\\  
   ( o.o ) 
   > ^.^ <
   /  * *  \\
  /  /   \\ \\
 /  /     \\ \\
    🎅
        """,
    """
    /\_/\\  
   ( ^.^ ) 
   > ^.^ <
   /  * *  \\
  /  /   \\ \\
 /  /     \\ \\
    🎁
        """
"]

def get_random_cat():
    all_cats = CATS + HACKER_CATS + SPECIAL_CATS + SLEEPING_CATS + PLAYFUL_CATS + HALLOWEEN_CATS + CYBERPUNK_CATS + CHRISTMAS_CATS
    return random.choice(all_cats)

def get_hacker_cat():
    return random.choice(HACKER_CATS + CYBERPUNK_CATS)

def get_special_cat():
    return random.choice(SPECIAL_CATS)

def get_sleeping_cat():
    return random.choice(SLEEPING_CATS)

def get_playful_cat():
    return random.choice(PLAYFUL_CATS)

def get_halloween_cat():
    return random.choice(HALLOWEEN_CATS)

def get_christmas_cat():
    return random.choice(CHRISTMAS_CATS)

def get_cyberpunk_cat():
    return random.choice(CYBERPUNK_CATS)

def get_seasonal_cat():
    import datetime
    month = datetime.datetime.now().month
    
    if month == 12:  
        return get_christmas_cat()
    elif month == 10:  
        return get_halloween_cat()
    else:
        return get_random_cat()

def get_themed_cat(theme=None):
    if theme == "hacker":
        return get_hacker_cat()
    elif theme == "special":
        return get_special_cat()
    elif theme == "sleeping":
        return get_sleeping_cat()
    elif theme == "playful":
        return get_playful_cat()
    elif theme == "halloween":
        return get_halloween_cat()
    elif theme == "christmas":
        return get_christmas_cat()
    elif theme == "cyberpunk":
        return get_cyberpunk_cat()
    elif theme == "seasonal":
        return get_seasonal_cat()
    else:
        return get_random_cat()

def get_all_cats():
    return {
        "regular": CATS,
        "hacker": HACKER_CATS,
        "special": SPECIAL_CATS,
        "sleeping": SLEEPING_CATS,
        "playful": PLAYFUL_CATS,
        "halloween": HALLOWEEN_CATS,
        "christmas": CHRISTMAS_CATS,
        "cyberpunk": CYBERPUNK_CATS
    }
