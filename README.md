# HYBRID RECOMMENDER SYSTEM

# İş Problemi

* ID'si verilen kullanıcı için item-based ve user-based recommender yöntemlerini kullanarak tahmin yapmak

# Veri Seti Hikayesi

* Veri seti, bir film tavsiye hizmeti olan MovieLens tarafından sağlanmıştır.İçerisinde filmler ile birlikte bu filmlere yapılan derecelendirme puanlarını 
barındırmaktadır.
* 27.278 filmde 2.000.0263 derecelendirme içermektedir. 
* Bu veriler 138.493 kullanıcı tarafından 09 Ocak 1995 ile 31 Mart 2015 tarihleri arasında oluşturulmuştur. Bu veri seti ise 17 Ekim 2016 tarihinde oluşturulmuştur.
* Kullanıcılar rastgele seçilmiştir. Seçilen tüm kullanıcıların en az 20 filme oy verdiği bilgisi mevcuttur.

# Değişkenler

# movie.csv
* movieId – Eşsiz film numarası. (UniqueID)
* title – Film adı

# rating.csv

* userid – Eşsiz kullanıcı numarası. (UniqueID)
* movieId – Eşsiz film numarası. (UniqueID)
* rating – Kullanıcı tarafından filme verilen puan
* timestamp – Değerlendirme tarihi

# Item-Based Collaborative Filtering

   ![image](https://user-images.githubusercontent.com/73841520/122440513-4d65c200-cfa5-11eb-83b7-7754e0c6571f.png)

* Item'ların productların diğer ifadesiyle filmlerin benzerlikliği üzerinden öneriler yapılır.
* İnput kullanıcıdan alınır ama iş birliğini tüm kullanıcılardan alınır. Filmleri için beğenilme davranışlarına odaklanır.

# User-Based Collaborative Filtering
* User benzerlikleri üzerinden öneriler yapılır.
* Odak noktası kullanıcı
