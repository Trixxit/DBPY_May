import disnake
from disnake.ext import commands 

def user_has_role(member: disnake.Member, role_ids: tuple):
    try:
        member_role_ids = {role.id for role in member.roles}
        return any(role_id in member_role_ids for role_id in role_ids)
    except:
        return []
    
def isStaff(member: disnake.Member):
    member_role_ids = {role.id for role in member.roles}
    return any(role_id in member_role_ids for role_id in staff_roles) or member.id == 776940844728057928 

def isAdmin(member: disnake.Member):
    member_role_ids = {role.id for role in member.roles}
    return any(role_id in member_role_ids for role_id in admin_roles) or member.id == 776940844728057928 

def isStaffOrGuide(member: disnake.Member):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in all_staff) or member.id == 776940844728057928 

def isMod(member: disnake.Member):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in mod_roles) or member.id == 776940844728057928 

def isLGOA(member: disnake.Member):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in staff_roles_and_lead_guides) or member.id == 776940844728057928 

def isMSE(member: disnake.Member):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in mod_eval) or member.id == 776940844728057928 

def isMLSE(member: disnake.Member):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in mod_lead_eval) or member.id == 776940844728057928 
def modle():
    async def predicate(ctx):
        if isMLSE(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def staffCheck():
    async def predicate(ctx):
        if isStaff(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def staffguideCheck():
    async def predicate(ctx):
        if isStaffOrGuide(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def modcheck():
    async def predicate(ctx):
        if isMod(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def admincheck():
    async def predicate(ctx):
        if isAdmin(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def leadguidecheck():
    async def predicate(ctx):
        if isLGOA(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)

def modevalcheck():
    async def predicate(ctx):
        if isMSE(ctx.author):
            return True
        elif ctx.author.id == 776940844728057928:
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)


def hasroles(member: disnake.Member, ids):
    mri = {role.id for role in member.roles}
    return any(role_id in mri for role_id in ids) or member.id == 776940844728057928



def Anystaffcheck(ids):
    async def predicate(ctx):
        if hasroles(ctx.author, ids):
            return True
        raise commands.CheckFailure("You do not have the required staff role to use this command.")
    return commands.check(predicate)
        


staff_roles = (
    971704489520300032, # Admin
    1183808147568210050, # CM
    971704672278675456, # Mod
    1178888662465917031, # Mod Trainee
    1186624610469421076, #LCM
    1231831222930636800, # mace

    )

all_staff = (
    971704489520300032, # Admin
    971704672278675456, # Mod
    1186624610469421076, #LCM
    1180945644567941272, # Lead Guide
    1183808147568210050, # CM
    1178888662465917031, # Mod Trainee
    1180235184747057162, # Guides
    )

admin_roles = (
    971704489520300032, # Admin
    1186624610469421076, # LCM
    )

mod_roles = (
    971704489520300032, # Admin
    971704672278675456, # Mod
    1186624610469421076, #LCM
    1178888662465917031 #trainee
)

staff_roles_and_lead_guides = (
    1186624610469421076, #LCM
    971704489520300032, # Admin
    1180945644567941272 # Lead Guide
)

mod_eval = (
    971704672278675456,
    1191893059970011276,
    1186624610469421076,
    971704489520300032,
)

mod_lead_eval = (
    971704672278675456,
    1191893059970011276,
    1186624610469421076,
    971704489520300032,
    1196465778438963392,
    1178888662465917031,
)

me = 1137611032311902299 
#776940844728057928

admin = 971704489520300032
mod = 971704672278675456
lcm = 1186624610469421076
trainee = 1178888662465917031
cm = 1183808147568210050
guide = 1180235184747057162
headguide = 1180945644567941272
subeval = 1191893059970011276
leadguide = 1191889241127538870
leadeval = 1196465778438963392
maycest = 1231831222930636800