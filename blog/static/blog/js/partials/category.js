function getContrastColor(hexColor) {
    hexColor = hexColor.replace('#', '');

    let r = parseInt(hexColor.substring(0, 2), 16);
    let g = parseInt(hexColor.substring(2, 4), 16);
    let b = parseInt(hexColor.substring(4, 6), 16);

    let brightness = (r * 299 + g * 587 + b * 114) / 1000;

    return brightness > 125 ? '#000000' : '#FFFFFF';
}

let categoryElement = document.querySelector('.post-category');

let bgColor = categoryElement.style.backgroundColor;

bgColor = rgbToHex(bgColor);

categoryElement.style.color = getContrastColor(bgColor);

function rgbToHex(rgb) {
    let result = rgb.match(/\d+/g).map(function(x) {
        return parseInt(x).toString(16).padStart(2, '0');
    });
    return '#' + result.join('');
}