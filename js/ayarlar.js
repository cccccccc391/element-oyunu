// Oyunun kuralları ve sabit yazıları.
// Puanları, can sayısını ya da oyunun adını değiştirmek için yalnızca bu dosyayı düzenlemek yeterli.

export const AYARLAR = {
  oyunAdi: 'Element Oyunu',              // Çalışma adı: oyunun asıl adını öğrenciler koyacak
  altBaslik: 'Bu element neden burada?',
  canSayisi: 3,                          // Bu kadar yanlışta bölüm baştan başlar
  soruPuani: 10,                         // Her doğru cevabın puanı
  bonusMaddeSayisi: 5,                   // Bölüm sonundaki bonus turda sorulan madde sayısı
  bonusIlkHipotezPuani: 20,              // Deneyden önce kurulan hipotez doğruysa
  bonusDuzeltmePuani: 10,                // Deneyden sonra doğru cevaba geçilirse
  // Soru türlerinin ne sıklıkla çıkacağı (sayı büyüdükçe o tür daha sık çıkar, 0 = hiç çıkmaz)
  soruTuruAgirliklari: { neden: 3, hangiElement: 2, isim: 1 },
};

export const HAKKINDA = [
  'Bu oyun bir TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projesi kapsamında hazırlanmaktadır.',
  'Element bilgileri, sorular ve bonus turundaki maddeler proje öğrencileri tarafından araştırılıp yazılmaktadır.',
  'Oyunun yazılım altyapısı, üretken yapay zekâ aracı Claude (Anthropic) desteğiyle geliştirilmiştir.',
  'Oyun hiçbir kişisel bilgi toplamaz. İlerlemeniz yalnızca bu cihazda saklanır.',
];
