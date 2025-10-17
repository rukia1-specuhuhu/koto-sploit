"""Collection of ASCII cat art for Kotosploit"""

import random

CATS = [
    r"""
        /\_/\  
       ( o.o ) 
        > ^ <
       /|   |\
      (_|   |_)
    """,
    r"""
    |\---/|
    | ,_, |
     \_`_/-..----.
  ___/ `   ' ,""+ \  
 (__...'   __\    |`.___.';
   (_,...'(_,.`__)/'.....+
    """,
    r"""
     /\_/\
    ( o   o )
    ==  Y  ==
      \   /
      /   \
     |     |
    """,
    r"""
       |\___/|
       )     (
      =\     /=
        )===(
       /     \
       |     |
      /       \
      \       /
    """,
    r"""
    /\___/\
   (  o o  )
   (  =^=  ) 
    )     (
   (       )
  (  (   (  )
 (__(__)___)
    """,
    r"""
     A_A
    (-.-)
     |-|  
    /   \
   |     |   _
   |  || |  | |
  /_||||  |_/ /
    """,
    r"""
    |\      _,,,---,,_
    /,`.-'`'    -.  ;-;;,_
   |,4-  ) )-,_..;\ (  `'-'
  '---''(_/--'  `-'\_)
    """,
    r"""
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
    r"""
     .       .
     |\_---_/|
    /   o_o   \
   |  \     /  |
   / '  \_/  ' \
  / .'"     "'. \
    """,
]

HACKER_CATS = [
    r"""
    (\__/)  ___
    (o^.^) |___|
    z(_(")(")  Hacking...
    """,
    r"""
     /\_/\     
    ( @.@ )  < Pentesting Mode
     > - <    
    /|   |\    
   (_|   |_)   
    """,
    r"""
    |\---/|
    | o_o |  << Exploiting...
     \_^_/
    """,
    r"""
    /\___/\
   (  ^w^  )  Security Cat
   (   =   )  is watching
    \  ~  /
    """,
]

def get_random_cat():
    return random.choice(CATS + HACKER_CATS)

def get_hacker_cat():
    return random.choice(HACKER_CATS)

def get_cute_cat():
    return random.choice(CATS)
