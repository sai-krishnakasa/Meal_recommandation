from app import food,engine,Session,meal_1000

local_session=Session()
items=[
    {
        'item':'BreakFast',
        'calories':''
    },

     {
        'item':'Milk (2 percent milk fat, 8 ounces)',
        'calories':122
    }
    ,
    {
        'item':'Egg (large, scrambled)',
        'calories':102
    }
    ,
    # {
    #      'item':'Apple(2)',
    #     'calories':150
    
    # },
    # {
    #      'item':'Banana(1)',
    #     'calories':105
    
    # },
    # # {
    # #      'item':'Beer(12 ounc)',
    # #     'calories':153
    
    # # },
    # # {
    # #     'item':"Bread(one slice)",
    # #     'calories':66
    # # },
    
    
   
    {
        'item':'Coffee (regular, brewed from grounds, black)',
        'calories':2
    },
    {
        'item':'Snack-1',
        'calories':''
    }
    ,
    {
        'item':'Carrots(raw,1-cup)',
        'calories':52
    
    },
    # ,
    # {
    #     'item':'Snack',
    #     'calories':''
    # }
    # ,
    #  {
    #      'item':'Chocolate chip cookie (from packaged dough)',
    #     'calories':59
    # }
    # ,
    {
        'item':'Lunch',
        'calories':''
    },
    {
        'item':'Chicken breast(3 ounces)',
        'calories':142
    },
    {
        'item':'Egg-Fried-Rice',
        'calories':300
    
    },
    # {
    #     'item':'Cola (12 ounces)',
    #     'calories':126
    # }
    # ,
    
    # ,
    # {
    #     'item':'Green beans (canned, drained, 1 cup)',
    #     'calories':40
    # }
    # ,
    {
        'item':'Ice cream (vanilla, 4 ounces)',
        'calories':145
    }
    ,
    # {
    #     'item':'Ketchup (1 tablespoon)',
    #     'calories':15
    # }
    # ,
   
    # ,
    # {
    #     'item':'Orange juice (frozen , 8 ounces)',
    #     'calories':112
    # }
    # ,
    # {
    #     'item':'Ice cream (vanilla, 4 ounces)',
    #     'calories':145
    # }
    # ,
    # {
    #     'item':'Pizza (pepperoni, regular crust, one slice)',
    #     'calories':298
    # }
    # ,
    # {
    #     'item':'Potato chips (plain, salted, 1 ounce)',
    #     'calories':155
    # }
    # ,
    # {
    #     'item':'Potato, medium (baked, including skin)',
    #     'calories':161
    # }
    # ,
    # {
    #     'item':'Raisins (1.5 ounces)',
    #     'calories':130
    # }
    # ,
    # {
    #     'item':'Red wine (cabernet sauvignon, 5 ounces)',
    #     'calories':123
    # }
    # ,
    # {
    #     'item':'Shrimp (cooked under moist heat, 3 ounces):',
    #     'calories':84
    # }
    # ,
    # {
    #     'item':'Snack-2',
    #     'calories':''
    # },
    # {
    #     'item':'pasta',
    #     'calories':110
    # }
    # ,
    {
        'item':'Dinner',
        'calories':''
    },
     {
        'item':'White-Boiled-rice',
        'calories':135
    }
    ,
    # {
    #     'item':'Brown-rice',
    #     'calories':135
    # }
    # ,
    {
        'item':'Red wine(sauvignon blanc, 1 ounce)',
        'calories':30
    }
    # ,
    # {
    #     'item':'White wine (sauvignon blanc, 5 ounces)',
    #     'calories':121
    # }
    # ,
    # {
    #     'item':'Yellow cake with chocolate frosting (one piece)',
    #     'calories':243
    # }
    # ,
    # {
    #     'item':'Spaghetti(cooked, enriched 1 cup)',
    #     'calories':221
    # }
    # ,
    # {
    #     'item':'Rice (long grain,cooked,1 cup)',
    #     'calories':205
    # }

    
]
local_session=Session(bind=engine)
for item in items:
    local_session.add(meal_1000(item=item['item'],calories=str(item['calories'])))
    
    local_session.commit()

    
