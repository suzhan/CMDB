// 请求参数转换
export function transformData(data) {
    let str = [];
    for (let key in data) {
        str.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    return str.join('&');
}