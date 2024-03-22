def fahrenheit_to_celcius(fahrenheit):
	return (fahrenheit - 32) * 5/9

def celcius_to_fahrenheit(celcius):
	return (clecius * 9/5) + 32

pilihan = input("\tPilih konversi suhu\n\n1. fahrenheit ke celcius\n2. celcius ke fahrenheit\n")

if pilihan == '1':
	fahrenheit = float(input("Masukkan nilai fahrenheit: "))
	celcius = fahrenheit_to_celcius(fahrenheit)
	print("{:.2f} Fahrenheit sama dengan {:.2f} Celcius".format(fahrenheit, celcius))
elif pilihan == '2':
	celcius = float(input("Masukkan nilai Celcius: "))
	fahrenheit = celcius_to_fahrenheit(celcius)
	print("{:.2f} Celcius sama dengan {:.2f} Fahrenheit".format(celcius, fahrenheit))
else:
	print ("Pilihan tidak valid. Pilih 1 atau 2")