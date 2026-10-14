# 🔍 Basit Port Tarayıcı

Python `socket` modülüyle yazılmış, eğitim amaçlı TCP connect tarayıcısı.

## Kullanım

```bash
python port_scanner.py                          # 127.0.0.1, port 1-1024
python port_scanner.py -t 192.168.1.10 -p 20-100
python port_scanner.py -t localhost -p 22,80,443
```

| Seçenek | Açıklama | Varsayılan |
|---------|----------|------------|
| `-t`, `--target` | Hedef IP veya alan adı | 127.0.0.1 |
| `-p`, `--ports` | Port veya aralık | 1-1024 |
| `--timeout` | Zaman aşımı (sn) | 0.5 |
| `--threads` | Eşzamanlı iş parçacığı | 100 |

Python 3.10 veya üstü gerekir, ek kurulum yoktur.

## Nasıl çalışır?

Her port için TCP bağlantısı kurmayı dener. Bağlantı kurulursa port açıktır. `ThreadPoolExecutor` ile portlar paralel taranır.

## Yasal uyarı

Yalnızca kendi makinende, kendi lab ortamında veya yazılı izin aldığın sistemlerde kullan. İzinsiz tarama suç sayılabilir. Program yerel olmayan hedeflerde izin teyidi ister.

## Geliştirme fikirleri

- [ ] Banner grabbing
- [ ] UDP tarama
- [ ] JSON / CSV çıktı
- [ ] Renkli terminal çıktısı

## Lisans

MIT
