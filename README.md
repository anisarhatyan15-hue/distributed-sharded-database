Distributed Sharded Database System with Automated Failover

Այս նախագիծը հորիզոնական ընդլայնվող (Horizontally Scalable) և վթարակայուն (Fault-Tolerant) տվյալների բազայի համակարգի սիմուլյացիա է՝ գրված **Python**-ով և **SQLite**-ով: Նախագծի նպատակն է ցուցադրել **Site Reliability Engineering (SRE)** և **Backend Architecture** հիմնական կոնցեպտները՝ տվյալների շարդավորումը (Sharding) և վթարից հետո ավտոմատ վերականգնումը (Failover):



Համակարգի Ճարտարապետությունը (Architecture)

Համակարգը բաղկացած է երեք ֆիզիկապես առանձնացված SQLite տվյալների բազաներից, որոնք կառավարվում են կենտրոնական Ռուտերի (Query Router) կողմից:

**`database_shard_1.db`** — Առաջին հիմնական բազան (Master Shard 1):
 **`database_shard_2.db`** — Երկրորդ հիմնական բազան (Master Shard 2):
 **`database_replica.db`** — Պահուստային համընդհանուր բազա (Asynchronous/Synchronous Replica):



1. Consistent Sharding (Կայուն Շարդավորում):** Տվյալների հավասարաչափ բաշխումն ապահովելու համար օգտատիրոջ `user_id`-ն անցնում է կրիպտոգրաֆիկ **MD5** հեշավորման միջոցով: Հեշի արդյունքը տեղափոխվում է $16$-ական համակարգ, և `% 2` (modulo) գործողությամբ որոշվում է թիրախային շարդը:
2. **Data Replication (Ռեպլիկացիա):** Տվյալների կորուստը բացառելու (Data Loss Prevention) նպատակով, ցանկացած `INSERT` գործողություն հիմնական շարդում հաջողվելուց հետո դուբլիկացվում է `database_replica.db`-ում:
3. **Automated Failover (Վթարի կառավարում):** Ընթերցման (`SELECT`) ժամանակ համակարգը ստուգում է բազայի առողջությունը (Health Check): Եթե հիմնական շարդն անհասանելի է, `try...except` բլոկը որսում է սխալը, և հարցումը ավտոմատ վերաուղղորդվում է դեպի Replica բազա:


