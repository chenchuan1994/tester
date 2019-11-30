import click
import os
from scene import manageScenario
import add_equipmeent



@click.group()
def easytester():
    pass

@easytester.command()
# build new scenario in workspace
@click.option('--new', '-n', 'newScenario', help = "Build a new scenario.")
# del scenario in workspace
@click.option('--del', '-d', 'delScenario', help = "Delete scenario.")

@click.option('--add', '-a', 'addEquip', help = "Add a equipment into scenario.")

# msg display
@click.option('--author')
def scenario(newScenario, delScenario, author, addEquip):
    "scenario in easytester"
    cwd = os.getcwd()  # workspace

    # deal new option(build scene)
    if newScenario == None:
        click.echo("Current workspace: %s" % cwd)
    else:
        click.echo("Current workspace: %s" % cwd)
        while(True):
            
            # if "\\" not in newScenario, may be path;else is folder
            if '\\' in newScenario:
                scname = input("Scenario name:")
                folder = newScenario
            else:
                scname = newScenario
                folder = cwd
            auth = input("author:")
            note = input("User note:")
            
            ask = input("Do you want to build a new scenario in here?[y/N]:")
            if ask in ('y', 'Y'):
                manageScenario.buildScenario(folder, scname, auth, note)
                break
            elif ask in ('n', 'N'):
                print("Stop building test scenarios.")
                break
            else:
                print("Error: invalid input")
    
    # deal del option
    if delScenario != None:
        print("try to del scenario")
    
    # deal message of scenario display
    if author != None:
        pass
        
    # add a new equipment into scenario
    if addEquip != None:
        add_equipmeent.add_equipment_into_scenario(addEquip)
        

@easytester.command()
@click.option('--equipment', '-e', 'equipment', help = "Show all equipments in scenario.")
def show(equipment):
    if equipment == None:
        equipment = "."
    print(equipment)
    add_equipmeent.show_equipment(equipment)

cli = click.CommandCollection(sources=[easytester])




if __name__ == "__main__":
    cli()