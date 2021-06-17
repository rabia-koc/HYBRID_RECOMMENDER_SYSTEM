#############################################
# PROJE: Hybrid Recommender System
#############################################
# ID'si verilen kullanıcı için item-based ve user-based recommender yöntemlerini kullanarak tahmin yapmak.


#############################################
# GÖREV 1: Verinin Hazırlanması
#############################################

import pandas as pd
pd.set_option('display.max_columns', 20)

movie = pd.read_csv('HAFTA_04/movie_lens_dataset/movie.csv')
rating = pd.read_csv('HAFTA_04/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
df.head()   # Burdaki tablonun oluşma şekli ratinglere puanlara göredir. yani verilen puanlara göre oluşturulmuş bir user birden fazla filme puan vermiş olabilir.

# Toplam yorum sayısı
df.shape

# Eşsiz film sayısı
df["title"].nunique()

# Hangi filme kaç yorum yapılmış:
df["title"].value_counts().head()

# 1000 üzeri film yapılan filmlerin seçilmesi:
comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["title"] <= 1000].index  # 1000'den daha az yoruma sahip olanlar.
common_movies = df[~df["title"].isin(rare_movies)] # rare_movies içindekiler değil
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
user_movie_df
user_movie_df.shape   # Yaklaşık 138 bin kullanıcının puan verdiği, yaklaşık 3 bin tane film var.
user_movie_df.columns
len(user_movie_df.columns)

common_movies["title"].nunique() # Azalma meydana geldi çünkü filtrelendi.

#############################################
# GÖREV 2: Öneri Yapılacak Kullanıcının İzlediği Filmlerin Belirlenmesi
#############################################

user = 108170
fm_user_df = user_movie_df[user_movie_df.index == user]   # Veri seti user'a göre indirgendi.
movies_watched = fm_user_df.columns[fm_user_df.notna().any()].tolist()
movies_watched  # Sadece kullanıcının izlediği filmler getirildi.
len(movies_watched)   # 186 tane film izlemiş

# Doğrulama işlemi:
user_movie_df.loc[user_movie_df.index == user, user_movie_df.columns == 'Sneakers (1992)']   # 4 puan vermiş.

#############################################
# GÖREV 3: Aynı Filmleri İzleyen Diğer Kullanıcıların Verisine ve Id'lerine Erişmek
#############################################

movies_watched_df = user_movie_df[movies_watched] # Sütun bazında filtreleme(fancy index)
movies_watched_df.head()  # Kullanıcının izlediği filmlere göre veri seti indirgendi.
movies_watched_df.shape  # User ile aynı filmi izleyen kullanıcılar.

user_movie_count = movies_watched_df.T.notnull().sum()  # Dolu olanların sum'ı alındı.
user_movie_count  # Her bir kullanıcının kaç tane film izlediği bilgisi.

user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]

perc = round(len(movies_watched) * 0.6)
users_same_movies = user_movie_count[user_movie_count["movie_count"]>perc]["userId"]   # Kullanıcı ile %60'dan fazla film izleyen kullanıclar.
users_same_movies.head()

user_movie_count[user_movie_count["movie_count"] > 130].count()  # Kullanıcı ile 130'dan film izleyen kullanıcıların sayısı.

#############################################
# GÖREV 4: Öneri Yapılacak Kullanıcı ile En Benzer Kullanıcıların Belirlenmesi
#############################################

final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      fm_user_df[movies_watched]])
final_df.head()  # User dahil ve diğer kullanıcılar

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']    # user_id_1: user, user_id_2: diğer kullanıcılar
corr_df = corr_df.reset_index()
corr_df.head()

# user ile yüzde 65 ve üzeri korelasyona sahip kullanıcılar:
top_users = corr_df[(corr_df["user_id_1"] == user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)  # User ile en yüksek korelasyona sahip olan kullanıcıları sıralandı.
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

# Kullanıcıların hangi filmlere kaç puan verdiğini görmek için rating tablosuna gidilmeli.
rating = pd.read_csv('HAFTA_04/movie_lens_dataset/rating.csv')
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')

# Görev 5'ten hemen önce top_user'dan user'ın kendisini çıkarmamız lazım:
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != user]

#############################################
# GÖREV 5: Weighted Average Recommendation Score'un Hesaplanması ve İlk 5 Filmin Tutulması
#############################################

# weighted_rating'in hesaplanması.
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings  # corr'dan dolayı değerlerde düşüş meydana geldi.

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})   # Filmlere göre tekilleştirme işlemi
recommendation_df = recommendation_df.reset_index()
recommendation_df.head()
recommendation_df.count()   # 2094 film için weighted_rating'ler mevcuttur.

# Kullanıcının bu filmler için vermesini beklediğimiz puanlar.
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)
movies_to_be_recommend

# Filmlerin isimlerini ekleme işlemi:
movie = pd.read_csv('HAFTA_04/movie_lens_dataset/movie.csv')
movies_to_be_recommend = movies_to_be_recommend.merge(movie[["movieId", "title"]])
movies_to_be_recommend

# Kullanıcının izlediği filmlerden en son en yüksek puan verdiği filmin adına göre user based öneri:
a_df = pd.DataFrame(movies_to_be_recommend["title"])
a_df.iloc[0:5]

#############################################
# GÖREV 6: Item-Based Recommendation(Kullanıcının izlediği filmlerden en son en yüksek puan verdiği filmin adına göre item-based öneri)
#############################################

# öneri yapılacak kullanıcının 5 puan verdiği filmlerden puanı en güncel olanı filmin id'sinin alınması:
movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)].sort_values(
    by="timestamp", ascending=False)["movieId"][0:1].values[0]

movie_name = df[df["movieId"]==movie_id]["title"].values[0]
movie_name

movie_name = user_movie_df[movie_name]   # user movie matrisinde bu filmi seçildi.

movies_from_item_based = user_movie_df.corrwith(movie_name).sort_values(ascending=False)   # Temel odak burası
# user movie matrisinde bu film ile korelasyonları getirildi.
# Burada tüm kullanıcların bir davranış birlikteliği vardır.

movies_from_item_based[1:6].index

