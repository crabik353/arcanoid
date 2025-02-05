Игра "Арканоид"

Проект представляет собой реализацию классической игры "Арканоид" с использованием библиотеки Pygame. 

Основные функции и возможности игры:

Игровой процесс: 
  Игрок управляет платформой, которая перемещается влево и вправо по нижней части экрана.
  Цель игры — отбивать мяч так, чтобы он уничтожал блоки, расположенные в верхней части экрана.
  Если мяч падает за пределы платформы, игра завершается, и игрок попадает в окно "Вы проиграли".
  Уровень считается пройденным, если все блоки уничтожены.
         
Уровни: 
  В игре доступно 8 уровней, каждый из которых усложняется увеличением количества блоков или их прочности.
  Новые уровни открываются последовательно: после успешного завершения текущего уровня становится доступен следующий.
      
Таймер и счет: 
  На каждом уровне отображается таймер, который показывает, сколько времени игрок затратил на прохождение.
  Счет увеличивается за каждый уничтоженный блок.
         
Пауза: 
  Во время игры можно нажать клавишу ESC, чтобы приостановить игру.
  В меню паузы доступны следующие опции:
        Продолжить игру.
        Перейти к выбору уровней.
        Открыть настройки.
        Вернуться в главное меню.
             
Настройки: 
  В разделе настроек можно:
        Включать/выключать музыку и звуковые эффекты.
        Изменять цвет платформы и мяча.
        Регулировать громкость музыки с помощью ползунка.
        Переключать музыкальные треки.
        Просмотреть управление в игре.
             
Окно управления: 
    В этом окне описаны основные клавиши управления:
        A/D или стрелки для движения платформы.
        Пробел для запуска мяча.
        ESC для паузы.
             
Звуки и музыка: 
    Игра включает звуковые эффекты для столкновений (удар мяча о платформу, блоки и стены).
    Фоновая музыка воспроизводится во время игры и может быть настроена в меню настроек.


Особенности реализации: 

  Классы и объекты: 
      Использованы классы для создания основных игровых объектов:
          Paddle — платформа, управляемая игроком.
          Ball — мяч, который отскакивает от платформы и блоков.
          Block — блоки, которые нужно уничтожить.
      Графический интерфейс: 
          Все текстовые элементы (счет, таймер, надписи) отрисовываются с помощью функции draw_text.
          Кнопки имеют визуальную обратную связь: изменяют цвет при наведении курсора.
