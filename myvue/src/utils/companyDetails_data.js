export default {
  image_modal: false,
  current_image_url: '',
  amac_manager: {},
  amac_product: {},
  is_amac_manager: false,
  is_amac_product: false,
  has_amac_info: false,
  amac_label: '',

  firm_id: '',
  full_data: {},

  /** 股东信息 */
  shareholder_cols: [{
    title: '股东',
    key: 'StockName',
    width: 'auto'
  },
  {
    title: '类型',
    key: 'StockType',
    width: 'auto'
  },
  {
    title: '持股比例',
    key: 'StockPercent',
    width: 'auto'
  },
  {
    title: '认缴出资额(万元)',
    key: 'ShouldCapi',
    width: 'auto'
  },
  {
    title: '认缴出资日期',
    key: 'ShoudDate',
    width: 'auto'
  }
  ],

  /** 工商变更 */
  businessChange_cols: [{
    title: '变更项目',
    key: 'ProjectName',
    width: 'auto'
  },
  {
    title: '变更日期',
    key: 'ChangeDate',
    width: 'auto'
  },
  {
    title: '变更前',
    key: 'BeforeContent',
    width: 'auto'
  },
  {
    title: '变更后',
    key: 'AfterContent',
    width: 'auto'
  }
  ],

  /** 异常列表 */
  abnormalInfo_cols: [{
    title: '列入日期',
    key: 'AddDate',
    width: 'auto'
  },
  {
    title: '异常原因',
    key: 'AddReason',
    width: 'auto'
  },
  {
    title: '列入决策机构',
    key: 'DecisionOffice',
    width: 'auto'
  },
  {
    title: '移出日期',
    key: 'RemoveDate',
    width: 'auto'
  },
  {
    title: '移出说明',
    key: 'RomoveReason',
    width: 'auto'
  },
  {
    title: '移出机构',
    key: 'RemoveDecisionOffice',
    width: 'auto'
  }
  ],

  /** 法律诉讼 */
  legalAction_cols: [{
    title: '被执行人信息',
    key: 'ExecutedPersonInfo',
    width: 'auto'
  },
  {
    title: '失信被执行人',
    key: 'ExecutedPerson',
    width: 'auto'
  },
  {
    title: '裁判文书',
    key: 'Referee',
    width: 'auto'
  },
  {
    title: '法院公告',
    key: 'CourtNotice',
    width: 'auto'
  },
  {
    title: '开庭公告',
    key: 'OpeningNotice',
    width: 'auto'
  },
  {
    title: '送达公告',
    key: 'DeliveryAnnouncement',
    width: 'auto'
  },
  {
    title: '股权冻结',
    key: 'EquityFreeze',
    width: 'auto'
  },
  {
    title: '立案信息',
    key: 'FilingInfo',
    width: 'auto'
  }
  ]
}
