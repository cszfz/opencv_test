import sys
import os

models=[['D:\\image\\model\\15rt.off','D:\\image\\model\\15lt.off'],
        ['D:\\image\\model\\2rt.off','D:\\image\\model\\2lt.off'],
        ['D:\\image\\model\\25rt.off','D:\\image\\model\\25lt.off'],
        ['D:\\image\\model\\3rt.off','D:\\image\\model\\3lt.off'],
        ['D:\\image\\model\\4rt.off','D:\\image\\model\\4lt.off']]
         

for model in models:
	r=open(model[0],'r')
	w=open(model[1],'w')
	l=r.readline()
	w.write(l)
	l=r.readline()
	w.write(l)

	l=l.strip('\n')
	t=l.split(' ')

	num=int(t[0])
	#print(num)
	for i in range(num):
		l=r.readline()
		t=l.split(' ')
		x=float(t[0])*(-1)
		#print(x)
		ll=str(x)+' '+t[1]+' '+t[2]+'\n'
		w.write(ll)
	l=r.readline()
	while l:
		w.write(l)
		l=r.readline()

	r.close()
	w.close()