import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

#### İş problemi

'''

Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne 
alternatif olarak yeni bir teklif türü olan "average bidding"’i tanıttı.

Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar 
verdi ve average bidding'in maximum bidding'den daha fazla dönüşüm getirip 
getirmediğini anlamak için bir A/B testi yapmak istiyor.

'''


#### Veri seti & Değişkenler

'''

Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra
buradan gelen kazanç bilgileri yer almaktadır. Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri
ab_testing.xlsx excel’inin ayrı sayfalarında yer almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average
Bidding uygulanmıştır.

Impression: Reklam görüntüleme sayısı
Click: Görüntülenen reklama tıklama sayısı
Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
Earning: Satın alınan ürünler sonrası elde edilen kazanç

'''

##############################################
## Görev 1: Veriyi Hazırlama ve Analiz Etme
##############################################

### Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

control = pd.read_excel("Miuul_Course_1/Measurement-Problems/Datasets/ab_testing.xlsx", sheet_name="Control Group")
control = control[["Impression", "Click", "Purchase", "Earning"]]
test = pd.read_excel("Miuul_Course_1/Measurement-Problems/Datasets/ab_testing.xlsx", sheet_name="Test Group")
test = test[["Impression", "Click", "Purchase", "Earning"]]

### Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_d = control.describe()
control.info()

test_d = test.describe()

fig, ax = plt.subplots()

ax.plot(control_d.index, control_d["Purchase"], color="red", marker="o")
ax.plot(test_d.index, test_d["Purchase"], color="blue", marker="s")

ax.legend(["Control", "Test"])

plt.show()

### Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df = pd.concat([control, test], axis=1)
df.columns = ['Impression', 'Click', 'Purchase', 'Earning', 'test_Impression', 'test_Click', 'test_Purchase', 'test_Earning']


##############################################
## Görev 2: A/B Testinin Hipotezinin Tanımlanması
##############################################

### Adım 1: Hipotezi tanımlayınız.

#### H0 : M1 = M2 Maximum bidding ve Average bidding uygulanan grupların yaptığı harcamalar arasında istatistiki olarak anlamlı bir fark yoktur.
#### H1 : M1 != M2 fark vardır.


### Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

df["Purchase"].mean()
df["test_Purchase"].mean()


##############################################
## Görev 3: Hipotez Testinin Gerçekleştirilmesi
##############################################

### Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
'''
Bunlar Normallik Varsayımı ve Varyans Homojenliğidir. Kontrol ve test grubunun normallik varsayımına uyup uymadığını 
Purchase değişkeni üzerinden ayrı ayrı test ediniz.
'''


#### Normallik varsayımı
##### h0: Normallik varsayımı sağlanmaktadır.
##### h1:  sağlanmamaktadır.

##### Control Grubu
test_stat, pvalue = stats.shapiro(df["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891 || p-value değeri 0.05 den küçük değildir. h0 reddedilemez.

##### Test Grubu
test_stat, pvalue = stats.shapiro(df["test_Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541 || p-value değeri 0.05 den küçük değildir. h0 reddedilemez.


#### Varyans Homojenliği
##### h0: Varyans homojendir
##### h1:  değildir.

test_stat, pvalue = stats.levene(df["Purchase"], df["test_Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083 || p-value değeri 0.05 den küçük değildir. h0 reddedilemez.



### Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

'''
Normallik varsayımı ve Varyans homojenliği varsayımı sağlandığını için "Bağımsız iki örneklem T testi uygulayacağız (parametrik test)"
'''

test_stat, pvalue = stats.ttest_ind(df["Purchase"], df["test_Purchase"], equal_var=True)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493




### Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki
### olarak anlamlı bir fark olup olmadığını yorumlayınız.

#### H0 : M1 = M2 Maximum bidding ve Average bidding uygulanan grupların yaptığı harcamalar arasında istatistiki olarak anlamlı bir fark yoktur.
#### H1 : M1 != M2 fark vardır.

'''
p-value değeri 0.05 den küçük olmadığı için H0 reddedilemez. 
'''



##############################################
## Görev 4: Sonuçların Analizi
##############################################

### Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

'''
Varsayımlar sağlandığı için bağımsız iki örneklem t testi yaptım. Bu test sonucunda p değeri 0.05'ten küçük olmadığı için H0 reddedilemedi. 
Sonuç olarak, Maximum Bidding ve Average Bidding teklifleri arasında anlamlı bir farklılık yoktur.
'''

