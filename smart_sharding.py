import sqlite3
import hashlib


shard_1_conn = sqlite3.connect("database_shard_1.db")
shard_2_conn = sqlite3.connect("database_shard_2.db")
replica_conn = sqlite3.connect("database_replica.db")

def init_databases():
    cursor1 = shard_1_conn.cursor()
    cursor2 = shard_2_conn.cursor()
    cursor_rep = replica_conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    );
    """

    cursor1.execute(create_table_query)
    cursor2.execute(create_table_query)
    cursor_rep.execute(create_table_query)

    shard_1_conn.commit()
    shard_2_conn.commit()
    replica_conn.commit()
    print("✅ [Initialization] Բոլոր 3 բազաները և աղյուսակները պատրաստ են։")


def get_shard(user_id):
    user_id_str = str(user_id)
    hash_object = hashlib.md5(user_id_str.encode())
    hash_hex = hash_object.hexdigest()
    hash_number = int(hash_hex, 16)
    shard_index = hash_number % 2

    if shard_index == 0:
        return "shard_1"
    else:
        return "shard_2"
    
def insert_user(user_id,name, email):

    target_shard = get_shard(user_id)
    insert_query = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)"

    if target_shard == "shard_1":
        cursor = shard_1_conn.cursor()
        cursor.execute(insert_query, (user_id, name, email))
        shard_1_conn.commit()
        print(f"📦 [Shard 1] Օգտատեր {name}-ը (ID: {user_id}) գրանցվեց Shard 1-ում։")
    else:
        cursor = shard_2_conn.cursor()
        cursor.execute(insert_query, (user_id, name, email))
        shard_2_conn.commit()
        print(f"📦 [Shard 2] Օգտատեր {name}-ը (ID: {user_id}) գրանցվեց Shard 2-ում։")
    replica_cursor = replica_conn.cursor()
    replica_cursor.execute(insert_query, (user_id, name, email))
    replica_conn.commit()
    print(f"🔄 [Replica] Օգտատեր {name}-ի տվյալները պատճենվեցին Replica-ում։")


def get_user_profile(user_id):
    target_shard = get_shard(user_id)
    query = "SELECT * FROM users WHERE id = ?"
    print(f"🔍 [Router] Որոնում ենք ID {user_id}-ը: Ալգորիթմը հուշում է, որ այն {target_shard}-ում է...")
    shard_is_healthy = False

    try:
            if not shard_is_healthy:
                raise sqlite3.OperationalError("🔥 Սերվերը անհասանելի է (Database Crash)!")
                
            if target_shard == "shard_1":
                cursor = shard_1_conn.cursor()
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
            else:
                cursor = shard_2_conn.cursor()
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                
            if result:
                print(f" [Success] Տվյալը հաջողությամբ վերցվեց {target_shard}-ից: {result}")
                return result
                
    except sqlite3.OperationalError as e:
        print(f"⚠️ [WARNING] {target_shard}-ը չպատասխանեց: Սխալ՝ {e}")
        print("🔄 [Failover] Ավտոմատ միանում ենք պահուստային Replica բազային...")
        
        replica_cursor = replica_conn.cursor()
        replica_cursor.execute(query, (user_id,))
        result = replica_cursor.fetchone()
        
        if result:
            print(f"🛡️ [Replica Success] Տվյալը ապահով փրկվեց Replica-ից: {result}")
            return result
            
    print(" Օգտատերը չգտնվեց և ոչ մի տեղ:")
    return None

init_databases()


print("\n---  Սկսում ենք տվյալների բաշխման թեստը ---")
insert_user(201, "Արմեն", "armen@mail.com")
insert_user(202, "Ալլա", "alla@mail.com")
insert_user(203, "Դավիթ", "davit@mail.com")
print("-------------------------------------------\n")
print("\n--- 🔍 Սկսում ենք տվյալների ընթերցման թեստը (Վթարի Սիմուլյացիա) ---")
get_user_profile(202)  # Փորձում ենք կարդալ Ալլայի տվյալները
print("-------------------------------------------\n")


