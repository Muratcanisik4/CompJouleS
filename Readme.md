# Enerji Ölçüm Örnekleri

Bu depo, çeşitli araçlar ve teknikler kullanarak enerji tüketimini ölçme konusundaki örnekleri ve açıklamaları içermektedir.

## Temel Kullanım

### Basit Bir Fonksiyonla Enerji Tüketimini Ölçme Örneği

Bir fonksiyonun enerji tüketimini ölçmek için, `energy_measurement` modülü tarafından sağlanan `measure_energy` dekoratörünü kullanabilirsiniz. İşte basit bir örnek:

```python
from energy_measurement import measure_energy

@measure_energy
def my_function():
    # Fonksiyonunuzun implementasyonu
    pass

my_function()
