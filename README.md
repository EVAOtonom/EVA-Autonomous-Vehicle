# Eva OTONOM AKS 2023-204 STM TEMELLİ ARAÇ KONTROL SİSTEMİ  

Merhaba değerli okuyucular bu dökümantasyon gelecek nesiller ve bu sene oldukça emek verilerek hazırlanmış olan araç kontrol sistemniniz klavuz dökümanatasyonudur.

Kod **Berkay Aşık, Samet Aygün ,Kaan Avcı, Esma Arhan, Emirhan Akdemir** Tarafından hazırlanmıştır.

Başlamadan önce eğer yeterince **temel programlama ve elektrik beceriniz** yok ise ilk önce bu konularda fikir sahibi olmanız ardından **STM_HAL** kütüphanesi ve **bit kaydırma** işlemlerinde temel bilgilere sahip olmanız gerekmektedir. Bu dökümantasyonu daha iyi anlamanızı sağlayacaktır.

## Araç Modları 

Aracımızda 4 adet moddan oluşmaktadır. 

|     *  |           Modlar   |  Anahtar | Button  |   |
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

Aynı zamanda kod içinde 40 derece içerisinde sınırlandırılmıştır.

**Wheel.c & Wheel.h** dosyaları içerisinde kullandığımız ve oluşturduğumuz komutlar ve fonksiyonlar ile tekerleklerin dönüşü sağlanmaktadır. Dönüş için **TIM12** den faydalanılmaktadır. İlgili direksiyon sisteminin H Bridge bağlantıları sağlanarak pwm üretilerek tekerler hareketi sağlanmaktadır.
Detaylı bilgi için kodları inceleyiniz.

> Tekerlekleri nasıl kontrol ediyoruz açı değerini nasıl veriyoruz ? Şu ana kadar genel olarak sizlere açı okumak ve dc motoru nasıl sürebileceğimizden ve nasıl sürdüğümüzden bahsettim.

**main.h** içerisinde bulunan header dosyasında


```c
typedef enum status_s {
	NoTurning,
	TurningRight,
	TurningLeft

}status_t;
typedef struct wheel_adjust_s{
	int16_t wantedDegree;
	int16_t wantedDegreeTemp;
	int16_t wheel_manuel;
	int16_t currrentDegree;
	int16_t currrentDegreeTemp;
	status_t status;
}wheel_adjust_t;

```
Bu kod bloğu içerisinde bir enum ve bir structure(C dilinde classlar sahip olmadığımız için tür topluluklarını tutmak için structure kullanırız) oluşturulmuştur.

* Typedef komutu bir struct değişkeninde tip tanımlamak için kullanılmıştır bu structe dan nesne oluştururken struct ön ekine ihtiyaç duymadan tanımladığımız **wheel_adjust_t** tip ile üretilir.

- **wantedDegreeTemp** değişkeni bizim direksiyon sistemine istediğimiz açı değerini göndererek döndürmemizi sağlamaktadır.
- **currentDegree** bu ise aracın şuan hangi açı değerinde olduğunu göstermektedir.
- **status** aracın ne tarafa döndüğünü enum vasıttasyıla bize gösterir.
- **wheel_manuel** şu an değinmiyeceğim fakat manuel sürüşte kullandığımız bir parametredir.

> Bu kısım samet abi tarafından oluşturulduğu için dilim döndükçe açıklamaya çalıştım. Umarım anlaşılır olmuştur


2. **Motor Sürücü**

Merhaba bu kısımda ise sizlere motor sürücü nedir ve neden aracımızda buna yer verdiğimizi anlatacağım.
Lütfen kendinizi salak gibi hissetmeyin veya oldukça akıllı neden bunlara değindiniz diye. **Bu yazıyı ileride okuyacak bilgi ve terim eksikliğine sahip arkadaşlarında okuyacağını unutmayınız.**

Motor sürücülerin temel prensibi elinizde bulunan dc,step,bldc motorları sürmenize olanak sağlayan bir parçadır. Bu parçanın içerisinde mosfet, mosfet sürücüleri, mikro kontrolcü ve kapasitör diyotlar yer almaktadır. Sürücüler türüne göre 80-90 Volta(Bu bilgi kelly için doğru olması gerekiyor değil ise güncelleyeceğim) kadar dayanabilmektedir. Aracımızda ise kelly marka oldukça güvenli bir hazır motor sürücüsü kullanmaktayızdır. 
Mosfetler 6'lı yada 12'li olabilmektedir. Mosfet sürücüleri mosfetleri(MOSFET= METAL OKSİT YARI İLETKEN ALAN ELEKTİK TRANSİSTÖRÜ' LERDİR) anahtarlamakta önemli görevler üstlenmekteidr. Belirli anahtarlamalar ile sürücüye göndermiş olduğumuz elektrik bir mıknatısları tetikleyerek motoru döndürmemizi sağlamaktadır.
Dataylı bilgi için bakabilirsiniz ama bunlar temel olarak neyin nasıl olduğunu bilmenizi istediğim için yazdım.

* Biz aracımız üzerinde bir bldc motor kullanmaktayız aynı zamanda bu motor hazır olarak kullanılmaktadır. 
* Kelly motor sürücü ise içerisinde bir yazılıma sahip olan ayarlanabilir ve sadece pwm vererek sürebildiğimiz bir sürücüdür. 

**bldc.c &bldc.h** içerisinde bulunan **adjustBldc** komutu ile 10 a kadar hız vererek aracı sürebilirsiniz.

- Bu kısımda **TIM14** kullanmaktayız

**main.c** içerisinde bulunan wantedSpeed parametresi ile araca hız değerleri göndererek tekerlek haraketi sağlamaktayız.

HAL_TIM_COMPARE komutu ile istediğimiz dutyCycle aralığında pwm üretebilmekteyizdir.

```c
__HAL_TIM_SET_COMPARE(&htim14,TIM_CHANNEL_1,speedValue);
```
Detaylı bilgi için lütfen kod içeriğini inceleyiniz.

3. **Fren Motoru & Switchler**


## Yazarlar
* **Kaan Avcı** - [github](https://github.com/kaanavcix)

