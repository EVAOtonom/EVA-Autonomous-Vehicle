#<<<<<<<<<<<<------ KALMAN FİLTRESİ HAKKINDA ------>>>>>>>>>>>>>>>>>>
#Kalman Filtresi, sistemin önceki durumlarına veya verilerine dayanarak, bir sonraki durumu veya veriyi en yüksek doğrulukta tahmin etmeyi amaçlar. 
#Özyinelemeli olarak çalışır. Temel olarak, Kalman Filtresi matematiksel olarak iki denklemle modellenir. Bunlar tahmin ve düzeltme denklemleridir. 
#Denklemlerin içerdiği değişkenler sensör gürültüsü, hata kovaryansı, işlem gürültüsü, Kalman kazancı, sensör verisi ve tahmin değişkenidir. 
#İlk eğitim için girdiğiniz hatalı veri, işlem gürültüsü ve hata kovaryansı kullanılarak gerçekleştirilir. Filtre, Kalman kazancı değerini hesaplar. 
#Ardından, Kalman kazancı değerini kullanarak yaptığı tahmini günceller. Son olarak, hata kovaryansını günceller ve bir sonraki veriyi güncel değişkenlerle birlikte tahmin eder, filtreler.
#Kalman kazancı değeri arttıkça filtrenin doğruluğu artar. Veri akışı devam ettiği sürece, filtre değişkenlerini güncelleme süreci devam eder. 
#Filtre, uygun parametrelerle ayarlanırsa ve eğitilirse, doğruluk oranını arttırarak çalışmaya devam eder. 
#Filtrenin eğitimi için, deneyimlerimize dayanarak, en yüksek doğrulukta alınan tahminleri esas alarak, eğitim parametrelerini belirledik. 
#Ardından, LİDAR sensörümüzden gelen verileri Kalman Filtresi'ne girdi olarak gönderdik.
#Filtrelenen tahmin çıktılarını kullanarak, parkur içinde aracımızın önünde yer alan engellerin ölçülerini ve aracımız ile engel arasındaki mesafeyi tespit ettik.

class KalmanFilter():
    def __init__(self,hataliOlcum,hataliTahmin,q):
        #KALMAN Kazancı ne kadar büyük olursa o kadar yavaş yaklaşacaktır.
        #KALMAN Kazancı ne kadar küçük olursa o kadar hızlı yaklaşır.
        #İki değeride arttırmak kalman kazancını küçültür. Tahmin değeri artarsa kalman daha çok küçülür.
        #Q değerini arttırmak tekrardan kalman kazancını küçültür.Yaklaşım hızlanır.
        self.olcumHatasi=hataliOlcum   # R matrisi-> sensör gürültüsü
        self.tahminHatasi=hataliTahmin # H matrisi-> hatalı ölçüm
        self.q=q                       # Q matrisi-> işlem gürültüsü
        self.guncelTahmin=0            # A matrisi-> güncel durum
        self.sonTahmin=0               # Son tahmin
        self.kalmanK=0                 # Kalman kazancı
        
    def tahminiGuncelle(self,olcum):
        self.kalmanK = self.tahminHatasi/(self.tahminHatasi+self.olcumHatasi)
        self.guncelTahmin=self.sonTahmin+self.kalmanK*(olcum-self.sonTahmin)
        self.tahminHatasi=(1-self.kalmanK)*self.tahminHatasi+ abs(self.sonTahmin-self.guncelTahmin)*self.q
        self.sonTahmin=self.guncelTahmin
        return self.guncelTahmin