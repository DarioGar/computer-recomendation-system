from api.v1 import con

class CPU:

    def __init__(self,name):
        self.name = name

    def register(self):
        cur = con.cursor()
        query = "INSERT INTO public.cpu (name) VALUES (%s) RETURNING id"
        cur.execute(query,(self.name))
        con.commit()
        return cur.fetchone()[0]

        
    @staticmethod
    def fetchAll():
        cur = con.cursor()
        query = "select * from public.cpu"
        cur.execute(query)
        rows = cur.fetchall()
        if(rows!=None):
            return rows
        else:
            return None
    
    @staticmethod
    def fetch(id):
        cur = con.cursor()
        query = "select name from public.cpu where id = %s"
        cur.execute(query,(id,))
        rows = cur.fetchone()
        if(rows!=None):
            return rows[0]
        else:
            return None