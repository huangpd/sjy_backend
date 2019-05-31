export default {
  image_modal: false,
  current_image_url: '',
  amac_manager: {},
  amac_product: {},
  is_amac_manager: false,
  is_amac_product: false,
  has_amac_info: false,
  amac_label: '',
  full_name: '这是导入的公司名称',
  firm_id: '',
  full_data: {},
  partner_list: [],
  change_list: [],
  exception_list: [],
  tax_list: [],
  partner_col_list: [{
    title: '股东',
    key: 'StockName',
    width: 200
  },
  {
    title: '类型',
    key: 'StockType',
    width: 200
  },
  {
    title: '持股比例',
    key: 'StockPercent',
    width: 200
  },
  {
    title: '认缴出资额(万元)',
    key: 'ShouldCapi',
    width: 200
  },
  {
    title: '认缴出资日期',
    key: 'ShoudDate',
    width: 200
  }
  ],
  change_col_list: [{
    title: '变更项目',
    key: 'ProjectName',
    width: 200
  },
  {
    title: '变更日期',
    key: 'ChangeDate',
    width: 200
  },
  {
    title: '变更前',
    key: 'BeforeContent'
  },
  {
    title: '变更后',
    key: 'AfterContent'
  }
  ],
  exception_col_list: [{
    title: '列入日期',
    key: 'AddDate',
    width: 100
  },
  {
    title: '异常原因',
    key: 'AddReason'
  },
  {
    title: '列入决策机构',
    key: 'DecisionOffice'
  },
  {
    title: '移出日期',
    key: 'RemoveDate',
    width: 100
  },
  {
    title: '移出说明',
    key: 'RomoveReason'
  },
  {
    title: '移出机构',
    key: 'RemoveDecisionOffice'
  }
  ],
  gudong_label: (h) => {
    return h('div', [
      h('span', '股东信息'),
      h('Badge', {
        props: {
          count: vue.partner_list.length,
          type: 'primary'
        }
      })
    ])
  },
  change_label: (h) => {
    return h('div', [
      h('span', '工商变更'),
      h('Badge', {
        props: {
          count: vue.change_list.length,
          type: 'primary'
        }
      })
    ])
  },
  exception_label: (h) => {
    return h('div', [
      h('span', '异常记录'),
      h('Badge', {
        props: {
          count: vue.exception_list.length,
          type: 'primary'
        }
      })
    ])
  }
}
