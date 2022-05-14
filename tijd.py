#tijd.py tijd in verschillende formaten
def u_dag(g):
    import time

    u = int(0)
    dag_uur = ' '
    
    W=time.strftime('%W')
#    print('week van het jaar',W)
    w=time.strftime('%w')
#    print('dag van de week',w) # 

    t = time.localtime()
    jaar = t[0]
    maand = t[1]
    dag = t[2]
    uur = t[3]
    minu = t[4]
    sec = t[5]
    u = t[3]
#    print(jaar)
#    print(maand)
#    print(dag)
#    print(u)
#    print(uur)
#    print(minu)
#    print(sec)

#    dag_uur = str(jaar) + '-' + str(maand) + '-' + str(dag) + ';' + str(W) + ';' + str(w) 
    jjjjmmdd = str(jaar) + '-' + str(f'{maand:02d}') + '-' + str(f'{dag:02d}')
#    print(jjjjmmdd)
    weekjaar = str(f'{int(W):02d}') 
#    print(weekjaar)
    weekdag = str(f'{int(w):02d}') 
#    print(weekdag)
    uu = str(f'{uur:02d}') 
#    print(uu)
    uummss = str(f'{uur:02d}') + ':' + str(f'{minu:02d}') + ':' + str(f'{sec:02d}')
#    print(uummss)
    dag_uur = jjjjmmdd  + ';' + weekjaar  + ';' + weekdag  + ';' + uummss  + ';' + jjjjmmdd + ' ' + uummss
    dag = str(jaar) + str(f'{maand:02d}') + str(f'{dag:02d}') 
#    print('dag : ',dag)
#    g[0]=uur
    g[0]=str(f'{uur:02d}')
    g[1]=dag_uur
#    g[2]=dag
    g[2]=str(f'{uur:02d}')
#    print(dag)
#    print(g)
    return g

    
    
