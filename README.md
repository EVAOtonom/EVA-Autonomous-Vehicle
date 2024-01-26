# Eva OTONOM AKS 2023-204 STM TEMELLİ ARAÇ KONTROL SİSTEMİ  

Merhaba değerli okuyucular bu dökümantasyon gelecek nesiller ve bu sene oldukça emek verilerek hazırlanmış olan araç kontrol sistemniniz klavuz dökümanatasyonudur.

Kod **Berkay Aşık, Samet Aygün ,Kaan Avcı, Esma Arhan, Emirhan Akdemir** Tarafından hazırlanmıştır.

Başlamadan önce eğer yeterince **temel programlama ve elektrik beceriniz** yok ise ilk önce bu konularda fikir sahibi olmanız ardından **STM_HAL** kütüphanesi ve **bit kaydırma** işlemlerinde temel bilgilere sahip olmanız gerekmektedir. Bu dökümantasyonu daha iyi anlamanızı sağlayacaktır.

## Araç Modları

Aracımızda 4 adet moddan oluşmaktadır. 

| Modlar |                    |  Anahtar | Button  |   |
|--------|--------------------|---|---|---|
| Mod1   | Otonom Araç Modu   |   Anahtar OFF|  Button OFF |   |
| Mod2   | Manuel Sürüş Modu  |  Anahtar ON |  Button OFF |   |
| Mod3   | Uzaktan Sürüş Modu |  Anahtar OFF | Button ON  |   |

Modların geçişleri 1.-2. modlar anahtar vasıtasıyla 3. mod ise açma kapama butonu ile aktif hale getirilmektedir. 

+ Araç içerisinde aynı zamanda private mod bulunmaktadır. Lütfen o modu eğer çekirdek takımda değilseniz kullanmayınız!.

## Otonom Sürüş Modu
Nedir bu otonom sürüş modu diye sorabilirsiniz. Geçmiş senelerde arduino ile devam etmiş olduğumuz temel mikrodenetleyici bize oldukça güçlü zorluklar çıkarmıştır. 
1. **Neden Ardunio yerine STM32 kullanıyoruz**

Temel olarak ardunio 256kb hafızaya 16mhz hıza sahiptir. STM32 ise 180mhz hıza çıkabiliyoruz. buda bizi oldukça hızlı veri işleme ve veri kontrol etme imkanı sunmaktadır.

2. **Otonom Sürüş Modu İçerği**
  
Otonom sürüş'ün olması gereken 3 ana etken vardır.  
- Absolute Rotary Encoder & Direksiyon Motoru (Direksiyon Sistemi)
- Motor Sürücü
- Fren Motoru & Switchler
- Röle sistemi 
> Röle sistemini (Bahsettğim şey röle kartı ve bağlantılar) kullanma içeriğimiz geri vites, acil stop ,ve ışıklandırma kontrolü içindir.

Bunların araç kontrol sisteminin temel parçaları olduğuna dair fikir sahibi olduğumuza göre bizim 2023 yılında üstünde oldukça düşündüğümüz ve sistemi oldukça iyi noktaya taşıdığımız. Direksiyon Sisteminden bahsetmek istiyorum.

1. **Direksiyon Sistemi**

Direksiyon sistemi 8 bitlik absolute enkoder ile direksiyon sisteminin kontrollü çalışması ile oluşturulmuştur. 

İnterupt (Kesme) fonksiyonu kullanılarak her durum tetiklenmesinde fonksiyon içerisine girerek tetikleme sağlanmaktadır.

Aşağıda ilgili kod örneğini koyarak durumu daha ifade etmek istiyorum.

```c
 wheelParameters.currrentDegreeTemp = (((GPIOC->IDR) >> 1) & 0x1FF);
		 wheelParameters.currrentDegreeTemp += wheel_offset;
		 if(wheelParameters.currrentDegreeTemp > 180) {
			 wheelParameters.currrentDegreeTemp -= 360;
		 }
		 wheelParameters.currrentDegreeTemp = wheelParameters.currrentDegreeTemp >> 2;
		 wheelParameters.currrentDegree = wheelParameters.currrentDegreeTemp;


```
Bu kısımda GPIOC pinin IDR registarına erişim sağlamaktayız IDR INPUT durumlarını tutan bir registerdır.
Bu registeda 1 bit kaydırılarak 1.bitten başlamış ve 9 bite kadar **0x1FF** ifadesi ile sınırlandırılmıştır.
& işareti burada 1 ile 9.bit arasındaki bitleri korur ve diğerlerini 0 olarak işaretler.
Ardından 360 derece okuma yapabildiğimiz enkoderi 180 den büyük olduğu durumda 360 derece çıkararak negatif sonucu elde ederiz. Ardından sağa dopru 2 bitlik şifleme yaparak elde ettiğimiz 180 derecelik açıyı 4 e bölmüş oluruz. ve 45 derecelik bir açı dilimi elde ederiz. Bunu yapma sebebimiz direksiyon açısının 40 derece ile sınırlı olacak şekilde ayarlamış olmamızdan kaynaklıdır. eğer 60 derece olsaydı o zaman direkt 3 e bölecektik.

Burada temel olarak mevut açı bilgisini almaktayız. Bu şekilde +45 ve -45 derecede olan açı değerlerini rahatlıkla 360lık dilim içerisinde okuyabilmekteyizdir.

**Wheel Offset** ise direksiyon motoruna enkoderi bağladığımızda başlganıç değeri değişmesi durumundan kaynaklı eklenmiştir. 2 bit shiftlediğimiz için -4 le çarpıp  +4 ekleyerek offsetin durumu toplanmalıdır. 







## Yazarlar
* **Kaan Avcı** - [github](https://github.com/kaanavcix)

