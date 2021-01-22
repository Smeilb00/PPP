from Codes import t1, t2, t3, t4, t5, t6, t7

print("Que programa quieres ejecutar:")
print("(Introducir número del 1 al 7)")
num = int(input())

if num == 1:
    t1.run()
elif num == 2:
    t2.run()
elif num == 3:
    t3.run()
elif num == 4:
    t4.run()
elif num == 5:
    t5.run()
elif num == 6:
    t6.run()
elif num == 7:
    print("Introducir nombre de la carpeta donde se encuentra la imagen:")
    inp = "\\" + str(input())
    print("Introducir nombre de la carpeta del datapool:")
    dat = "\\" + str(input())
    print("Introducir nombre la carpeta de salida:")
    out = "\\" + str(input())

    data = {
        "Input":inp,
        "Output":out,
        "Datapool": dat
    }
    t7.run(data)