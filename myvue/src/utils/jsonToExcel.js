export default {
  JSONToExcelConvertor (JSONData, FileName, ShowLabel) {
    // 先转化json
    var arrData = typeof JSONData !== 'object' ? JSON.parse(JSONData) : JSONData

    var excel = '<table>'
    // 设置表头
    var row = '<tr>'
    for (var i = 0, l = ShowLabel.length; i < l; i++) {
      row += '<td>' + ShowLabel[i] + '</td>'
    }
    // 换行
    excel += row + '</tr>'
    // 设置数据
    // eslint-disable-next-line no-redeclare
    for (var i = 0; i < arrData.length; i++) {
      // eslint-disable-next-line no-redeclare
      var row = '<tr>'

      for (var index in arrData[i]) {
        var value = arrData[i][index] === '.' ? '' : arrData[i][index]
        row += '<td>' + value + '</td>'
      }
      excel += row + '</tr>'
    }
    excel += '</table>'
    var excelFile = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:x='urn:schemas-microsoft-com:office:excel' xmlns='http://www.w3.org/TR/REC-html40'>"
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8">'
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel'
    excelFile += '; charset=UTF-8">'
    excelFile += '<head>'
    excelFile += '<!--[if gte mso 9]>'
    excelFile += '<xml>'
    excelFile += '<x:ExcelWorkbook>'
    excelFile += '<x:ExcelWorksheets>'
    excelFile += '<x:ExcelWorksheet>'
    excelFile += '<x:Name>'
    excelFile += '{worksheet}'
    excelFile += '</x:Name>'
    excelFile += '<x:WorksheetOptions>'
    excelFile += '<x:DisplayGridlines/>'
    excelFile += '</x:WorksheetOptions>'
    excelFile += '</x:ExcelWorksheet>'
    excelFile += '</x:ExcelWorksheets>'
    excelFile += '</x:ExcelWorkbook>'
    excelFile += '</xml>'
    excelFile += '<![endif]-->'
    excelFile += '</head>'
    excelFile += '<body>'
    excelFile += excel
    excelFile += '</body>'
    excelFile += '</html>'

    var uri = 'data:application/vnd.ms-excel;charset=utf-8,' + encodeURIComponent(excelFile)

    var link = document.createElement('a')
    link.href = uri

    link.style = 'visibility:hidden'
    link.download = FileName + '.xlsx'

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // var datas=[];
  // var grid=getCmp("grid");
  // var grid_data = grid.getStore();

  // for(var i= 0 ;i< grid_data.data.length;i++){ //获取extjs grid的数据
  // var row = grid_data.getAt(i).data;
  // datas.push({"列头1":row["OrgName"],...});
  // }

  // var datas = [{
  //   key: value
  // }......];

  // JSONToExcelConvertor(datas, "汇总", ["列头1", "头2", "头3"]);
}
