# Лабораторная работа 1: Статическая маршрутизация

## Приложить скрипт - генератор конфигурации для всех устройств и сгенерированные им файлы конфигурации (в имени файла должно быть имя соотв. устройства)

Файл с примером конфигурации:
- [config.json](in%2Fconfig.json)

Скрипт выполняющий генерацию конфигураций формата `frr.conf`:
- [config_generator.py](config_generator.py)

## Приложить скрипт-парсер нужных команд по выводу состояния устройств (show команды+ping/traceroute)

Скрипт [commands.py](commands.py), поддерживаемые команды:
- run -> `show run`
- routes -> `show ip routes`
- brief -> `show interface brief`
- route -> `show ip route {ip}`
- ping -> `ping -c 10 -W 1 {ip}`
- traceroute -> `traceroute -m 10 {ip}`

## По п.1.2.3 своими словами написать несколько предложений, отвечающих на вопрос и объясняющих ситуацию c приложением подкрепляющих выводы show команд.

Рассмотрим 2 пути, из PC1 в PC2 и в PC3.

### Данные о маршруте до PC2
```shell
PC1# show ip route 192.168.22.4
Routing entry for 192.168.22.0/24
  Known via "static", distance 1, metric 0, best
  Last update 01w0d21h ago
  * 192.168.11.1, via eth1, weight 1
```

### Данные о маршруте до PC3
```shell
PC1# show ip route 192.168.33.4
Routing entry for 192.168.33.0/24
  Known via "static", distance 1, metric 0, best
  Last update 01w0d21h ago
  * 192.168.11.1, via eth1, weight 1
```

Видим, что для PC1 маршрут одинаковый, нужно идти на роутер.

Рассмотрим маршруты из роутера.

### Данные о маршруте до PC2 из R1

```shell
router1# show ip route 192.168.22.4
Routing entry for 0.0.0.0/0
  Known via "kernel", distance 0, metric 0, best
  Last update 01w1d21h ago
  * 172.20.20.1, via eth0
```


### Данные о маршруте до PC3 из R1

```shell
router1# show ip route 192.168.33.4
Routing entry for 192.168.33.0/24
  Known via "static", distance 1, metric 0, best
  Last update 01w0d21h ago
  * 192.168.2.3, via eth2, weight 1
```

Видим, что R1 не знает о маршруте до PC2 и даже не может определить подсеть.
