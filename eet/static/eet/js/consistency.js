$(document).ready(function () {
    $('.x-items').change(
        function () {
            var clickedRadio = this;
            var afterClickedRadio = false;

            var radios = $('.x-items');

            for (i = 0; i < radios.length; ++i) {
                var radio = radios[i];

                if (radio === clickedRadio) {
                    afterClickedRadio = true;
                    continue;
                }

                if (!afterClickedRadio && clickedRadio.value === 'R' && radio.value === 'R') {
                    radio.checked = true;
                }
                if (afterClickedRadio && clickedRadio.value === 'L' && radio.value === 'L') {
                    radio.checked = true;
                }
            }
        }
    );
});

$(document).ready(function () {
    $('.y-items').change(
        function () {
            var clickedRadio = this;
            var afterClickedRadio = false;

            var radios = $('.y-items');

            for (i = 0; i < radios.length; ++i) {
                var radio = radios[i];

                if (radio === clickedRadio) {
                    afterClickedRadio = true;
                    continue;
                }

                if (!afterClickedRadio && clickedRadio.value === 'R' && radio.value === 'R') {
                    radio.checked = true;
                }
                if (afterClickedRadio && clickedRadio.value === 'L' && radio.value === 'L') {
                    radio.checked = true;
                }
            }
        }
    );
});