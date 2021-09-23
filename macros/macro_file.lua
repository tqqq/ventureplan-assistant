
-- 1. print role info
/run print(string.format("##ROLE_DATA##{\"name\":\"%s-%s\", \"anima\":%s}##", UnitName("player"), GetRealmName(), C_CurrencyInfo.GetCurrencyInfo(1813).quantity))

-- ------------------

-- 2. logout
/logout

-- ------------------

-- 3. open copychat window
/run CCP.openCcpCopyFrame(i);

-- ------------------

-- 4. assign and clear chat
/run for i = 1, NUM_CHAT_WINDOWS do _G[format("ChatFrame%d", i)]:Clear() end;CovenantMissionFrame.MissionTab.MissionPage["StartMissionButton"]:Click()
/click StaticPopup1Button1
/click StaticPopup1Button2

-- ------------------








