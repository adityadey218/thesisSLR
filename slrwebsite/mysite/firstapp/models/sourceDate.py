class SourceData:


    def __init__(self):
        self.SJRList = []
        self.SNIPList = []
        self.citeScoreCurrentMetric = None
        self.citeScoreTracker = None


    def parseSourceDataArrayFromJson(self, jsonSourceData, journal_title):
        print(journal_title)
        print("rand")
        if not jsonSourceData:
            return None

        if len(jsonSourceData) == 0:
            return []
        resultListOfSourceData = []
        root = jsonSourceData["serial-metadata-response"]
        root_test = root
        if "error" not in root_test:
            entryList = root["entry"]

            for entry in entryList:
              if entry["dc:title"] == journal_title:
               sourceData = SourceData()
               resultListOfSourceData.append(sourceData)
               if "SNIPList" in entry.keys():
                if "SNIP" in entry["SNIPList"].keys():
                    for snip in entry["SNIPList"]["SNIP"]:
                        sourceData.SNIPList.append({"year": int(snip["@year"]), "value": snip["$"]})
                else:
                   sourceData.SNIPList.append({"year": int(0), "value": 0})
               else:
                 sourceData.SNIPList.append({"year": int(0), "value": 0})

               if "SJRList" in entry.keys():
                if "SJR" in entry["SJRList"].keys():
                    for sjr in entry["SJRList"]["SJR"]:
                        sourceData.SJRList.append({"year": int(sjr["@year"]), "value": sjr["$"]})
                else:
                   sourceData.SJRList.append({"year": int(0), "value": 0})
               else:
                 sourceData.SJRList.append({"year": int(0), "value": 0})

               if "citeScoreYearInfoList" in entry.keys():
                keys = entry["citeScoreYearInfoList"].keys()
                if "citeScoreCurrentMetric" in keys and "citeScoreCurrentMetricYear" in keys:
                    if entry["citeScoreYearInfoList"]["citeScoreCurrentMetric"] is not None:
                        sourceData.citeScoreCurrentMetric = \
                          {
                            "year": int(entry["citeScoreYearInfoList"]["citeScoreCurrentMetricYear"]),
                            "value": entry["citeScoreYearInfoList"]["citeScoreCurrentMetric"]
                          }
                    else:
                        sourceData.citeScoreCurrentMetric = \
                            {
                                "year": 0,
                                "value": 0
                            }
                if "citeScoreTracker" in keys and "citeScoreTrackerYear" in keys:
                    if entry["citeScoreYearInfoList"]["citeScoreTracker"] is not None:

                      sourceData.citeScoreTracker = \
                        {
                            "year": int(entry["citeScoreYearInfoList"]["citeScoreTrackerYear"]),
                            "value": entry["citeScoreYearInfoList"]["citeScoreTracker"]
                        }
                    else:
                      sourceData.citeScoreTracker = \
                        {
                            "year": 0,
                            "value": 0
                        }
               else:
                    sourceData.citeScoreCurrentMetric = \
                        {
                            "year": 0,
                            "value": 0
                        }
                    sourceData.citeScoreTracker = \
                        {
                            "year": 0,
                            "value": 0
                        }
            #resultListOfSourceData.append(sourceData)
        return resultListOfSourceData
