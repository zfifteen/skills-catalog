=== 0 BASELINE (no keys) ===
  ADDR_LINE: 			20 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.comhttps//grok.com
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: 'https://grok.comhttps//grok.com'

=== 1 ONLY Meta+l ===
  ADDR_LINE: 			18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.comhttps//grok.com, Placeholder: Search or enter website name
  Selected text: [https://grok.comhttps//grok.com]
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: 'https://grok.comhttps//grok.com, Placeholder: Search or enter website name'

=== 2 ONLY Meta+a (after Meta+l) ===
  ADDR_LINE: 			18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.comhttps//grok.com, Placeholder: Search or enter website name
  Selected text: [https://grok.comhttps//grok.com]
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: 'https://grok.comhttps//grok.com, Placeholder: Search or enter website name'

=== 3 type ONE char 'X' (does it replace or append?) ===
  ADDR_LINE: 			18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.comhttps//grok.comX, Placeholder: Search or enter website name
  ADDR_LINE: The focused UI element is 18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.comhttps//grok.comX, Placeholder: Search or ent
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: 'https://grok.comhttps//grok.comX, Placeholder: Search or enter website name.'

=== 4 Meta+l again, then Meta+a, then Backspace ===
  ADDR_LINE: 			19 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Placeholder: Search or enter website name
  ADDR_LINE: The focused UI element is 19 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Placeholder: Search or enter website name.
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: None

=== 5 type_text 'https://example.com' into cleared field ===
  ADDR_LINE: 			18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://example.com, Placeholder: Search or enter website name
  ADDR_LINE: The focused UI element is 18 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://example.com, Placeholder: Search or enter website na
  TAB_URL: https://grok.comhttps//grok.com
  ADDR_VALUE: 'https://example.com, Placeholder: Search or enter website name.'

=== 6 Return ===
  ADDR_LINE: 			22 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://example.com
  TAB_URL: https://example.com/
  ADDR_VALUE: 'https://example.com'

=== 7 set_value on address field (if we can find index) ===
  found address field index: 22 line=			22 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: htt
  ADDR_LINE: 			22 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://grok.com/
  TAB_URL: https://example.com/
  ADDR_VALUE: 'https://grok.com/'
  (set_value alone does NOT navigate — need Return if value stuck)
  ADDR_LINE: 			22 text field (settable, string) Description: smart search field ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD, Value: https://example.com
  TAB_URL: https://example.com/
  ADDR_VALUE: 'https://example.com'