import generate_model as gm

for x in range (0, 200):
    gm.gen_model(9, 1)
    print("Generating models: "+str((x/200)*100) + "% complete...")
