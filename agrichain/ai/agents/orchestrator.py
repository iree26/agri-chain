"""  
Orchestrator Agent - Fixed Language + Stable Production Version
"""

import os
import asyncio
import time
import logging
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from agrichain.ai.agents.soil_agent import SoilAgent
from agrichain.ai.agents.weather_agent import WeatherAgent
from agrichain.ai.agents.market_agent import MarketAgent
from agrichain.ai.agents.finance_agent import FinanceAgent
from agrichain.ai.utils.sanitizer import validate_all_inputs
from agrichain.ai.utils.soil_recommender import get_soil_recommendation, SOIL_TYPES, FERTILIZATION_METHODS
from agrichain.ai.utils.file_generator import save_farm_plan_files

env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)

logger = logging.getLogger(__name__)


class OrchestratorAgent:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.soil_agent = SoilAgent()
        self.weather_agent = WeatherAgent()
        self.market_agent = MarketAgent()
        self.finance_agent = FinanceAgent()

    # -----------------------------
    # SAFE WRAPPER
    # -----------------------------
    async def safe_run(self, coro, timeout, fallback):
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except Exception:
            return fallback

    # -----------------------------
    # DISPATCHERS
    # -----------------------------
    async def dispatch_soil_agent(self, state, lga, crop):
        start = time.time()
        result = await self.safe_run(
            self.soil_agent.analyze_soil(state, lga, crop),
            timeout=8,
            fallback=f"Soil suitable for {crop} in {state}."
        )
        return result, time.time() - start

    async def dispatch_weather_agent(self, state, lga, crop):
        start = time.time()
        result = await self.safe_run(
            self.weather_agent.analyze_weather(state, lga, crop),
            timeout=8,
            fallback=f"Stable weather expected in {state}."
        )
        return result, time.time() - start

    async def dispatch_market_agent(self, crop, state, farm_size):
        start = time.time()
        result = await self.safe_run(
            self.market_agent.analyze_market_prices(crop, state, farm_size),
            timeout=6,
            fallback=f"Monitor {crop} market prices."
        )
        return result, time.time() - start

    async def dispatch_finance_agent(self, crop, farm_size, state):
        start = time.time()
        result = await self.safe_run(
            self.finance_agent.analyze_financing(crop, farm_size, state),
            timeout=6,
            fallback="Check BOA or cooperative loans."
        )
        return result, time.time() - start

    # -----------------------------
    # LANGUAGE FIX (IMPORTANT)
    # -----------------------------
    def get_language_instruction(self, language: str) -> str:
        language_map = {
            "English": "IMPORTANT: Respond ONLY in English. Do not mix languages.",
            "Yoruba": "IMPORTANT: Respond ONLY in Yoruba language. Every sentence must be Yoruba.",
            "Hausa": "IMPORTANT: Respond ONLY in Hausa language. Every sentence must be Hausa.",
            "Igbo": "IMPORTANT: Respond ONLY in Igbo language. Every sentence must be Igbo."
        }
        return language_map.get(language, "IMPORTANT: Respond ONLY in English.")



    def get_fallback_farm_plan(self, crop: str, state: str, language: str,
                               soil_type="Loamy", fertilization_method="Mixed"):
        fallback_plans = {
            "English": f"""
1. FARM OBJECTIVES
- Establish a productive and sustainable {crop} farm spanning the available land area.
- Achieve food security and generate steady income for the farmer and family.
- Implement modern and traditional farming techniques for optimal yield.
- Build a resilient farming operation that can withstand climate and market fluctuations.
- Expand operations over time and create employment opportunities in the local community.

2. LAND AND SITE ANALYSIS
- The farm is located in {state}, which has suitable agro-ecological conditions for {crop} cultivation.
- Soil type is {soil_type}, which provides adequate drainage and nutrient-holding capacity.
- Assess the land for proper drainage, slope, and water retention before planting.
- Conduct a soil pH test to confirm whether lime or sulfur amendments are needed.
- Evaluate water sources — rainfall patterns, nearby streams, or borehole availability.
- Consider wind direction and sun exposure when planning field orientation.

3. FARM LAYOUT AND DESIGN
- Divide the farm into sections: main crop area, nursery beds, compost zone, and storage area.
- Allocate 70% of land to main {crop} production, 10% to nursery, 10% to pathways and buffer zones, and 10% to storage and equipment shed.
- Install a central irrigation system with branching channels or drip lines to each section.
- Build access roads wide enough for farm machinery and harvest transport.
- Position storage facilities near the main access road for easy loading and offloading.
- Create windbreaks using fast-growing trees around the farm perimeter.

4. PRODUCTION STRATEGY
- Begin with land clearing, tilling, and bed preparation 2–3 weeks before planting.
- Source high-quality, disease-resistant {crop} seeds from certified suppliers.
- Apply pre-planting fertilizer based on soil test recommendations for {soil_type} soil.
- Plant at the correct spacing and depth for {crop} to ensure optimal growth.
- Implement a regular irrigation schedule: 2–3 times per week depending on rainfall.
- Monitor for common pests and diseases weekly; apply organic or chemical control as needed.
- Weed control: manual weeding every 2 weeks or use of mulch to suppress weed growth.
- Harvest at the right maturity stage to maximize quality and market price.
- Post-harvest handling: sort, clean, and store in a cool, dry place.

5. EQUIPMENT AND RESOURCES NEEDED
- Land preparation: tractor or hoe, plough, harrow, ridger.
- Planting: hand planters, measuring tape, markers, watering cans.
- Irrigation: pump, pipes, sprinklers or drip lines, water storage tank.
- Crop maintenance: knapsack sprayer, pruning shears, machete, hoe, rake.
- Harvesting: harvesting crates, baskets, knives, weighing scale.
- Storage: ventilated storage room, gunny bags, pallets.
- Inputs: certified seeds, NPK fertilizer, organic compost, pesticides, herbicides.
- Protective gear: boots, gloves, face masks, overalls.

6. LABOUR PLAN
- Farm manager/supervisor: 1 person (full-time) — oversees all farm operations.
- Permanent farm workers: 2–3 persons (full-time) — planting, irrigation, maintenance.
- Seasonal workers: 4–6 persons (part-time during planting and harvest seasons).
- Roles: land preparation crew, planting team, irrigation operators, pest control team, harvesters.
- Provide basic training on crop management, equipment use, and safety procedures.
- Labour cost estimate: include wages, meals, and accommodation if applicable.

7. FINANCIAL PLAN
- Startup costs: land preparation, equipment purchase, seeds, fertilizers, irrigation setup.
- Operating costs: labour, water, electricity, fuel, pesticides, transportation, maintenance.
- Contingency fund: set aside 10–15% of total budget for emergencies.
- Revenue projection: estimate yield per hectare × expected market price per unit.
- Break-even analysis: calculate the point at which total revenue covers total costs.
- Funding sources: personal savings, Bank of Agriculture loans, cooperative society loans, government agricultural grants.
- Maintain a simple ledger to track all income and expenses.

8. MARKETING PLAN
- Target markets: local open markets, urban wholesalers, supermarkets, food processors.
- Pricing strategy: monitor market prices weekly and price competitively.
- Distribution: transport harvested {crop} directly to market or use collection centers.
- Storage: use proper storage to avoid post-harvest losses and sell when prices are favourable.
- Build relationships with buyers: offer consistent quality and reliable supply.
- Consider value addition: cleaning, packaging, or processing to increase income.
- Record sales data to identify best-performing markets and seasons.
""",
            "Yoruba": f"""
1. AWỌN IBI-ÀFẸMỌ́ Ọ̀GBIN
- Ṣe ìdásílẹ̀ oko {crop} tó ṣe é gbéṣẹ́ tó sì ń so èso dáradára.
- Rí i pé oúnjẹ wà fún ìdílé àti pé owó ń wọlé dáradára.
- Lo àwọn ìlànà òde-òní àti ìbílẹ̀ láti gba èso tó pọ̀.
- Kó oko le kọjà àwọn ìyipada ojú ọjọ́ àti ọjà.
- Gbìyànjú láti mú oko gbòòrò kí ó sì dá àwọn iṣẹ́ sílẹ̀ fún àgbègbè.

2. ÌTÚPALẸ̀ ILẸ̀ ÀTI IBÌ
- Oko wà ní {state}, ibi tí ojú ọjọ́ àti ilẹ̀ rẹ̀ bá {crop} mu.
- Iru ilẹ̀ ni {soil_type}, tó ń da omi nù dáradára tó sì ń gba afẹ́fẹ́.
- Ṣàyẹ̀wò ilẹ̀ fún ìmú omi, ìtẹ́ ilẹ̀ àti agbára idaduro omi.
- Wọn ipele pH ilẹ̀ láti fi mọ̀ bóyá kílààtì tàbí sulfur yẹ.
- Ṣàyẹ̀wò orísun omi — iye òjò, àwọn odò, tàbí kànga.
- Kíyèsi ìtọ́nà afẹ́fẹ́ àti ìmọ́lẹ̀ oòrùn nígbà tí o ń gbòòrò oko.

3. ÌTÒ ÀTI ÌGBÉKALẸ̀ OKO
- Pín oko sí àwọn apá: ibi gbín, ibi itọ́jú, ibi compost, àti ibi ìpamọ́.
- Fi 70% ilẹ̀ fún gbín {crop}, 10% fún ibi itọ́jú, 10% fún ọ̀nà, 10% fún ibi ìpamọ́.
- Fi eto irigeson sílẹ̀ pẹ̀lú àwọn ọ̀nà omi tó lọ sí gbogbo apá oko.
- Kọ́ àwọn ọ̀nà tó gbóòrì tó fún àwọn ẹ̀rọ àti kẹ̀kẹ́.
- Gbé ibi ìpamọ́ sí ibi tó rọrùn fún kíkó ẹrù sí ọkọ̀.
- Gbin àwọn igi tó ń da afẹ́fẹ́ ní àyíká oko.

4. ÌGBÉRÒ ÌṢÈJÁDE
- Bẹ̀rẹ̀ pẹ̀lú ìmọ́ ilẹ̀, ìtu ilẹ̀, àti ìṣe ibi gbín 2–3 ọ̀sẹ̀ ṣáájú gbín.
- Ra irúgbin {crop} tó dáradára, tó lè kojú àrùn.
- Fi ajile ṣáájú gbín gẹ́gẹ́ bí ìmọ̀ràn ilẹ̀ rẹ̀ fún {soil_type}.
- Gbin ni ààyè àti ìjìnlẹ̀ tí ó tọ́ fún {crop}.
- Mú eto irigeson dé: 2–3 ìgbà lọ́sẹ̀ gẹ́gẹ́ bí òjò.
- Ṣàyẹ̀wò àwọn kòkòrò àti àrùn lọ́sẹ̀-ọ̀sẹ̀; fi ìràwọ̀ tàbí ògùn tí ó tọ́.
- Pa èpò: máa pa èpò lọ́wọ́ lọ́sẹ̀-ọ̀sẹ̀ tàbí lo mulch.
- Kórè ní ìgbà tí èso bá pọ́n dáradára.
- Lẹ́yìn ìkórè: tọ́jọ́, wẹ, kó si ibi tó tutù.

5. ÀWỌN Ẹ̀RỌ ÀTI OHUN-ÈLÒ TÍ A NILÒ
- Ìmúra ilẹ̀: trátòr tàbí ọ̀kà, plough, harrow, ridger.
- Gbín: àwọn ẹ̀rọ gbín, tépù, àmì, ìgò omi.
- Ìrìgèsón: póńpù, píìpù, sprinkles tàbí drip lines, ìgò omi nla.
- Ìtọ́jú: knapsack sprayer, pruning shears, àdá, ọ̀kà, rake.
- Ìkórè: agbọn, agbọ̀n, ọ̀bẹ, òṣùwọ̀n.
- Ìpamọ́: yàrá ìpamọ́, àpò, pallets.
- Ohun èlò: irúgbin, NPK ajile, compost, ògùn kòkòrò, ògùn èpò.
- Àwọ̀tílẹ̀: bàtà, ìbọ̀wọ́, ìbòjú, aṣọ.

6. ÈTÒ ÒSÌṢẸ́
- Olùṣọ́ oko: 1 (kún-akókò) — ń bójú tó gbogbo iṣẹ́ oko.
- Àwọn òṣìṣẹ́ aláìṣiṣẹ́pọ̀: 2–3 (kún-akókò) — gbín, irigeson, ìtọ́jú.
- Àwọn òṣìṣẹ́ ìgbà: 4–6 (apá-akókò nígbà gbín àti ìkórè).
- Àwọn iṣẹ́: ìmọ́ ilẹ̀, ẹgbẹ́ gbín, ẹgbẹ́ irigeson, ẹgbẹ́ ìtọ́jú, ẹgbẹ́ ìkórè.
- Pese ìdánilẹ́kọ̀ọ́ lórí ìtọ́jú {crop}, lílo ẹ̀rọ, àti ààbò.
- Iye owó òṣìṣẹ́: owó iṣẹ́, oúnjẹ, ibùgbé.

7. ÈTÒ ÌSÚNÁWÓ
- Iye owó ìbẹ̀rẹ̀: ìmúra ilẹ̀, rírà ẹ̀rọ, irúgbin, ajile, irigeson.
- Iye owó iṣiṣẹ́: òṣìṣẹ́, omi, iná, epo, ògùn, gbigbé, ìtọ́jú.
- Ifowó pàmọ́: fi 10–15% àyà gbà fún ìjábá.
- Àsọtẹ́lẹ̀ owó tí ń wọlé: iye èso fun hektà × iye owó tí a ń tà.
- Ìtúpalẹ̀ break-even: ibi tí owó tí ń wọlé bá tó owó tí a ná.
- Orísun owó: ifowópamọ́, Bank of Agriculture, awin ẹgbẹ́, ìrànlọ́wọ́ ìjọba.
- Pa ìwé-àkọọ́lẹ̀ owó mọ́.

8. ÈTÒ ÒWÒ
- Ọjà: ọjà gbogbo ènìyàn, àwọn olùrà túndùn, ilé-iṣọ́, ilé-ìjẹun.
- Ìgbérò owó: ṣàyẹ̀wò owó ọjà lọ́sẹ̀-ọ̀sẹ̀ kí o sì fi owó tó bójú mu.
- Gbigbékó: gbé {crop} lọ sí ọjà tàbí ibi ìkójọpọ̀.
- Ìpamọ́: lo ìpamọ́ tí ó tọ́ láti má bàa pàdánù.
- Kó àjọṣe pẹ̀lú olùrà: pese didára àti ìgbà gbà-ìgbà.
- Ṣiṣẹ́ afikun: wẹ, bá àpò, ṣe èlò láti gba owó púpọ̀.
- Kọ àkọọ́lẹ̀ ojà láti mọ ibi tí owó ń wọlé jù.
""",
            "Hausa": f"""
1. MANUFOFIN GONA
- Kafa gona {crop} mai albarka da dorewa.
- Samar da abinci da kuma samun kuɗi mai kyau ga manomi da iyalinsa.
- Yi amfani da fasaha na zamani da na gargajiya don samun amfanin gona mai yawa.
- Gina gona mai ƙarfi don jure wa sauyin yanayi da kasuwa.
- Fadada ayyukan a tsawon lokaci da samar da ayyukan yi ga al'umma.

2. NAZARIN KASA DA WURI
- Gona tana cikin {state}, inda yanayi ya dace don noman {crop}.
- Irin ƙasa: {soil_type}, wanda ke da magudanar ruwa mai kyau.
- Bincika ƙasa don magudanar ruwa, tudu, da kuma riƙon ruwa kafin shuka.
- Gwada pH na ƙasa don sanin ko ana buƙatar lemun ƙasa ko sulfur.
- Bincika tushen ruwa — yanayin ruwan sama, kogi, ko rijiyar burtsatse.
- Yi la'akari da alkiblar iska da hasken rana yayin shimfida gona.

3. TSARI DA SHIRI GONA
- Raba gona zuwa sassa: babban yankin shuka, wurin dasa, wurin taki, da wurin ajiya.
- Sanya 70% na ƙasa don noman {crop}, 10% na wurin dasa, 10% na hanyoyi, 10% na ajiya.
- Sanya tsarin ban ruwa mai rassa zuwa kowane sashi.
- Gina hanyoyi masu faɗi don injuna da jigilar girbi.
- Sanya wurin ajiya kusa da babbar hanya don sauƙin ɗaukar kaya.
- Gina shingen iska ta amfani da bishiyoyi masu saurin girma.

4. DABARUN SAMARWA
- Fara da share ƙasa, noma, da shirya gadaje 2–3 makonni kafin shuka.
- Samo iri {crop} ingantattun, masu juriya daga attajirai.
- Sanya taki kafin shuka bisa ga gwajin ƙasa don {soil_type}.
- Shuka da daidai tazara da zurfin da ya dace don {crop}.
- Sanya tsarin ban ruwa na yau da kullun: sau 2–3 a mako.
- Duba kwari da cututtuka kowane mako; yi amfani da magani.
- Cire ciyawa duk sati biyu ko yi amfani da mulch.
- Girbe a daidai lokacin balaga don inganci da farashi.
- Bayan girbi: tsara, tsaftace, adana a wuri mai sanyi.

5. KAYAN AIKI DA ALBOBUN DA AKE BUKATA
- Shirye-shiryen ƙasa: tarakta ko fartanya, garma, harrow, ridger.
- Shuka: injunan shuka, tef, alamomi, feshin ruwa.
- Ban ruwa: famfo, bututu, sprinklers ko drip lines, tankin ruwa.
- Kula da shuka: knapsack sprayer, pruning shears, adda, fartanya, rake.
- Girbi: kwanduna, kwanduna, wuƙaƙe, ma'auni.
- Ajiya: ɗakin ajiya, buhunan gunny, pallets.
- Albo: iri, NPK taki, taki na halitta, maganin kwari, maganin ciyawa.
- Kayan kariya: takalmi, safofin hannu, abin rufe fuska, tufafi.

6. TSARIN MA'AIKATA
- Mai kula da gona: mutum 1 (cikakken lokaci) — kula da dukkan ayyuka.
- Ma'aikatan dindindin: mutum 2–3 (cikakken lokaci) — shuka, ban ruwa, kula.
- Ma'aikatan yanayi: mutum 4–6 (lokacin shuka da girbi).
- Ayyuka: share ƙasa, shuka, ban ruwa, maganin kwari, girbi.
- Ba da horo kan kula da {crop}, amfani da kayan aiki, da aminci.
- Kudin ma'aikata: albashi, abinci, masauki.

7. TSARIN KUɗI
- Kudin farawa: share ƙasa, siyan kayan aiki, iri, taki, ban ruwa.
- Kudin gudanarwa: ma'aikata, ruwa, wutar lantarki, mai, magunguna, sufuri, kulawa.
- Asusun gaggawa: ajiye 10-15% na kasafin kuɗi don gaggawa.
- Hasashen kuɗin shiga: yawan amfanin gona a kowace hekta × farashin kasuwa.
- Binciken break-even: lokacin da kuɗin shiga ya rufe kuɗin da aka kashe.
- Tushen kuɗi: ajiyar kai, Bank of Agriculture, lamunin hadin gwiwa, tallafin gwamnati.
- Rike lissafin kuɗi na yau da kullun.

8. TSARIN KASUWANCI
- Kasuwar da aka yi niyya: kasuwannin gida, manyan dillalai, manyan kantuna, masu sarrafa abinci.
- Dabarun farashi: duba farashin kasuwa kowane mako.
- Rarraba: kai {crop} kai tsaye zuwa kasuwa ko wuraren tattarawa.
- Ajiya: yi amfani da ajiya mai kyau don guje wa hasara.
- Gina dangantaka da masu saye: samar da inganci akai-akai.
- Ƙara darajar: tsaftacewa, tattarawa, ko sarrafawa don ƙarin kuɗi.
- Rubuta bayanan tallace-tallace don gano mafi kyawun kasuwa.
""",
            "Igbo": f"""
1. IHE EGWU NZUỤTA UBỊ
- Guzobere ubi {crop} na-adịgide adịgide nke na-amị mkpụrụ nke ọma.
- Nweta nchekwa nri na ego na-abata nke ọma nye onye ọrụ ugbo na ezinụlọ ya.
- Jikọta usoro ugbo ọgbara ọhụrụ na nke ọdịnala iji nweta mkpụrụ kachasị mma.
- Wulite ọrụ ugbo siri ike nke nwere ike iguzogide mgbanwe ihu igwe na ahịa.
- Gbasaa ọrụ ka oge na-aga ma mepụta ohere ọrụ n'ime obodo.

2. NYOCHA ALA NA EBE
- Ubi dị na {state}, ebe ọnọdụ ihu igwe kwesịrị ekwesị maka ịkọ {crop}.
- Ụdị ala bụ {soil_type}, nke na-enye ezigbo mgbapụta mmiri na njide nri.
- Nyochaa ala maka mgbapụta mmiri, mkpọda, na njide mmiri tupu ịkụ ihe.
- Nwalee pH ala iji kwado ma ọ bụrụ na achọrọ lime ma ọ bụ sulfur.
- Tụlee isi mmiri — usoro mmiri ozuzo, iyi, ma ọ bụ olulu mmiri dị.
- Tụlee ntụzịaka ifufe na ìhè anyanwụ mgbe ị na-ahazi ubi.

3. NHỌZI NA IHE E SI KWỌỌ UBÌ
- Kewaa ubi na ngalaba: ebe ịkụ ihe, ebe ịzụlite, ebe compost, na ebe nchekwa.
- Kenye 70% ala maka ịkọ {crop}, 10% maka ịzụlite, 10% maka ụzọ, 10% maka nchekwa.
- Wụnye usoro ịgba mmiri nke nwere alaka na-eru na ngalaba ọ bụla.
- Wuo ụzọ sara mbara iji kwado igwe ugbo na ibugharị ihe ubi.
- Doo ebe nchekwa n'akụkụ ụzọ mbata maka ịkwanye ngwa ngwa.
- Mepụta ihe mgbochi ifufe site na iji osisi na-eto ngwa ngwa gburugburu ubi.

4. USORO MMEPỤTA
- Malite na ikpochapụ ala, ịkọ ala, na ịkwadebe ihe ndina 2-3 izu tupu ịkụ ihe.
- Nweta mkpụrụ {crop} dị mma, na-eguzogide ọrịa site n'aka ndị ahịa ndị a pụrụ ịtụkwasị obi.
- Tinye fatịlaịza tupu ịkụ ihe dabere na nnwale ala maka {soil_type}.
- Kụọ n'ebe dị anya na omimi ziri ezi maka {crop}.
- Mee usoro ịgba mmiri oge niile: ugboro 2-3 kwa izu dabere na mmiri ozuzo.
- Nyochaa maka pests na ọrịa kwa izu; tinye ọgwụ organic ma ọ bụ chemical dịka achọrọ.
- Igbo ahịhịa: jiri aka wepụ ahịhịa kwa izu abụọ ma ọ bụ jiri mulch.
- Gbute n'ogo ntozu kwesịrị ekwesị iji bulie ogo na ọnụahịa.
- Njikwa mgbe owuwe ihe ubi gasịrị: dozie, hichaa, chekwaa na ebe jụrụ oyi.

5. NGWA ỌRỤ NA AKỤ NGWA ACHỌRỌ
- Nkwadebe ala: traktọ ma ọ bụ shọvelu, plough, harrow, ridger.
- Ịkụ ihe: ihe ịkụ ihe, teepu, ihe nrịbama, iko mmiri.
- Ịgba mmiri: pọmpụ, paịpụ, sprinklers ma ọ bụ eriri ntanye, tankị mmiri.
- Nlekọta ihe ubi: knapsack sprayer, pruning shears, mma, shọvelu, rake.
- Owuwe ihe ubi: nkata, nkata, mma, ihe ọ̀tụ̀tụ̀.
- Nchekwa: ụlọ nchekwa, akpa gunny, pallets.
- Ihe ntinye: mkpụrụ ndị gbasara, NPK fatịlaịza, compost, ọgwụ pests, ọgwụ ahịhịa.
- Ngwá ọrụ nchebe: akpụkpọ ụkwụ, uwe aka, ihe mkpuchi ihu, uwe.

6. ATỤMATỤ NDỌ ỌRỤ
- Onye nlekọta ubi: mmadụ 1 (oge niile) — na-elekọta ọrụ ubi niile.
- Ndị ọrụ oge niile: mmadụ 2–3 (oge niile) — ịkụ ihe, ịgba mmiri, nlekọta.
- Ndị ọrụ oge: mmadụ 4–6 (oge ịkụ ihe na owuwe ihe ubi).
- Ọrụ: ndị na-akọ ala, ndị ịkụ ihe, ndị ịgba mmiri, ndị na-ahụ maka pests, ndị owuwe ihe ubi.
- Nye ọzụzụ banyere nlekọta {crop}, ojiji ngwa ọrụ, na nchekwa.
- Atụmatụ ụgwọ ọrụ: ụgwọ ọrụ, nri, ebe obibi.

7. ATỤMATỤ EGO
- Ụgwọ mmalite: nkwadebe ala, ịzụta ngwa ọrụ, mkpụrụ, fatịlaịza, ịgba mmiri.
- Ụgwọ arụmọrụ: ndị ọrụ, mmiri, ọkụ, mmanụ, ọgwụ pestis, njem, mmezi.
- Ego nchekwa: debe 10–15% nke mmefu ego niile maka ihe mberede.
- Amụma ego nbata: atụmatụ mkpụrụ kwa hekta × ọnụahịa ahịa.
- Nyocha break-even: mgbe ego nbata ruru mkpokọta mmefu.
- Isi ego: ego nchekwa onwe, Bank of Agriculture, mbinye ego ọgbakọ, enyemaka gọọmentị.
- Debe akwụkwọ ndekọ ego.

8. ATỤMATỤ AHỊA
- Ahịa ezubere: ahịa obodo, ndị na-ere ahịa n'obodo mepere emepe, nnukwu ụlọ ahịa, ndị na-ahazi nri.
- Usoro ọnụahịa: lelee ọnụahịa ahịa kwa izu wee tọọ ọnụahịa asọmpi.
- Nkesa: buru {crop} gaa ahịa ma ọ bụ ebe nchịkọta.
- Nchekwa: jiri ebe nchekwa dị mma iji zere ọnwụ.
- Wulite mmekọrịta na ndị na-azụ ahịa: nye ogo na-agbanwe agbanwe.
- Tụlee mgbakwunye uru: ihicha, nkwakọba, ma ọ bụ nhazi iji nweta ego ka ukwuu.
- Dee data ahịa iji chọpụta ahịa kachasị mma.
"""
        }
        return fallback_plans.get(language, fallback_plans["English"])

    # -----------------------------
    # SYNTHESIS LAYER (FIXED)
    # -----------------------------
    async def generate_farm_plan(
        self, name, state, lga, crop, farm_size,
        soil, weather, market, finance, language,
        soil_type="Loamy", fertilization_method="Mixed"
    ):

        language_instruction = self.get_language_instruction(language)

        soil_rec = get_soil_recommendation(soil_type, fertilization_method, crop)

        system_prompt = f"""
You are an expert agricultural advisor for Nigerian farmers.

{language_instruction}

CRITICAL RULE:
You MUST write the entire response strictly in the requested language.
Do NOT translate into English.
Do NOT mix languages.
All section headings must be in the requested language.

Generate a comprehensive, detailed, and elaborate farm plan. The plan must NOT be short or surface-level. It must read like a professional, well-developed farm plan with deep, actionable insights.

Include ALL of the following sections with clear headings translated into the requested language:

1. FARM OBJECTIVES — The vision, mission, and specific goals for this farm (short-term and long-term).
2. LAND AND SITE ANALYSIS — Detailed assessment of the land, soil characteristics, climate, water availability, and location advantages or challenges.
3. FARM LAYOUT AND DESIGN — How the farm should be organized: crop area divisions, irrigation layout, access roads, storage, and infrastructure placement.
4. PRODUCTION STRATEGY — Comprehensive step-by-step production plan covering land preparation, planting, crop management, pest and disease control, irrigation schedule, and harvesting.
5. EQUIPMENT AND RESOURCES NEEDED — Complete list of farming equipment, tools, machinery, inputs (seeds, fertilizers, pesticides), and other resources required.
6. LABOUR PLAN — Staffing requirements, roles and responsibilities, seasonal labour needs, and labour management strategy.
7. FINANCIAL PLAN — Detailed budget breakdown (startup costs, operating costs, contingency), revenue projections, break-even analysis, and funding sources.
8. MARKETING PLAN — Target markets, pricing strategy, distribution channels, storage and transportation, customer identification, and sales timeline.

Each section must be thorough, well-developed, and provide specific, actionable advice tailored to the farmer's crop, location, and farm size. Write multiple paragraphs per section with rich detail. Do not skip any section.
"""

        user_prompt = f"""
Farmer: {name}
Location: {lga}, {state}
Crop: {crop}
Farm Size: {farm_size} hectares

SOIL:
{soil}

WEATHER:
{weather}

MARKET:
{market}

FINANCE:
{finance}

SOIL TYPE: {soil_type}
FERTILIZATION METHOD: {fertilization_method}

FERTILIZATION RECOMMENDATION:
{soil_rec}
"""

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.6,
                max_tokens=4000
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self.get_fallback_farm_plan(crop, state, language, soil_type, fertilization_method)

    # -----------------------------
    # STREAMING SYNTHESIS LAYER (NEW)
    # -----------------------------
    async def generate_farm_plan_stream(
        self, name, state, lga, crop, farm_size,
        soil, weather, market, finance, language,
        stream_callback,
        soil_type="Loamy", fertilization_method="Mixed"
    ):
        """Generate farm plan with streaming and real-time callback."""

        language_instruction = self.get_language_instruction(language)

        soil_rec = get_soil_recommendation(soil_type, fertilization_method, crop)

        system_prompt = f"""
You are an expert agricultural advisor for Nigerian farmers.

{language_instruction}

CRITICAL RULE:
You MUST write the entire response strictly in the requested language.
Do NOT translate into English.
Do NOT mix languages.
All section headings must be in the requested language.

Generate a comprehensive, detailed, and elaborate farm plan. The plan must NOT be short or surface-level. It must read like a professional, well-developed farm plan with deep, actionable insights.

Include ALL of the following sections with clear headings translated into the requested language:

1. FARM OBJECTIVES — The vision, mission, and specific goals for this farm (short-term and long-term).
2. LAND AND SITE ANALYSIS — Detailed assessment of the land, soil characteristics, climate, water availability, and location advantages or challenges.
3. FARM LAYOUT AND DESIGN — How the farm should be organized: crop area divisions, irrigation layout, access roads, storage, and infrastructure placement.
4. PRODUCTION STRATEGY — Comprehensive step-by-step production plan covering land preparation, planting, crop management, pest and disease control, irrigation schedule, and harvesting.
5. EQUIPMENT AND RESOURCES NEEDED — Complete list of farming equipment, tools, machinery, inputs (seeds, fertilizers, pesticides), and other resources required.
6. LABOUR PLAN — Staffing requirements, roles and responsibilities, seasonal labour needs, and labour management strategy.
7. FINANCIAL PLAN — Detailed budget breakdown (startup costs, operating costs, contingency), revenue projections, break-even analysis, and funding sources.
8. MARKETING PLAN — Target markets, pricing strategy, distribution channels, storage and transportation, customer identification, and sales timeline.

Each section must be thorough, well-developed, and provide specific, actionable advice tailored to the farmer's crop, location, and farm size. Write multiple paragraphs per section with rich detail. Do not skip any section.
"""

        user_prompt = f"""
Farmer: {name}
Location: {lga}, {state}
Crop: {crop}
Farm Size: {farm_size} hectares

SOIL:
{soil}

WEATHER:
{weather}

MARKET:
{market}

FINANCE:
{finance}

SOIL TYPE: {soil_type}
FERTILIZATION METHOD: {fertilization_method}

FERTILIZATION RECOMMENDATION:
{soil_rec}
"""

        try:
            # Use streaming API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.6,
                max_tokens=4000,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Call callback with each chunk for real-time display
                    if stream_callback:
                        stream_callback(content)

            return full_response.strip()

        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            fallback = self.get_fallback_farm_plan(crop, state, language, soil_type, fertilization_method)
            if stream_callback:
                stream_callback(fallback)
            return fallback

    # -----------------------------
    # MAIN ORCHESTRATION
    # -----------------------------
    async def orchestrate(self, name, state, lga, crop, farm_size, language,
                          stream_callback=None, soil_type="Loamy",
                          fertilization_method="Mixed"):

        valid, inputs = validate_all_inputs(
            name, state, lga, crop, str(farm_size), language
        )

        if not valid:
            return {
                "success": False,
                "error": "Input validation failed",
                "details": inputs
            }

        name = inputs["name"]
        state = inputs["state"]
        lga = inputs["lga"]
        crop = inputs["crop"]
        farm_size = inputs["farm_size"]
        language = inputs["language"]

        if soil_type.title() not in [s.title() for s in SOIL_TYPES]:
            soil_type = "Loamy"
        soil_type = soil_type.title()

        print("Dispatching agents...")

        soil_task = self.dispatch_soil_agent(state, lga, crop)
        weather_task = self.dispatch_weather_agent(state, lga, crop)
        market_task = self.dispatch_market_agent(crop, state, farm_size)
        finance_task = self.dispatch_finance_agent(crop, farm_size, state)

        (soil, soil_t), (weather, weather_t), (market, market_t), (finance, finance_t) = await asyncio.gather(
            soil_task,
            weather_task,
            market_task,
            finance_task
        )

        print("Synthesizing farm plan...")

        synth_start = time.time()
        
        # Use streaming if callback provided, otherwise use regular generation
        if stream_callback:
            farm_plan = await self.generate_farm_plan_stream(
                name, state, lga, crop, farm_size,
                soil, weather, market, finance,
                language,
                stream_callback,
                soil_type, fertilization_method
            )
        else:
            farm_plan = await self.generate_farm_plan(
                name, state, lga, crop, farm_size,
                soil, weather, market, finance,
                language,
                soil_type, fertilization_method
            )
        
        synthesis_t = time.time() - synth_start

        print("\nFarm plan ready!")

        result = {
            "success": True,
            "farmer_name": name,
            "location": f"{lga}, {state}",
            "crop": crop,
            "farm_size": farm_size,
            "language": language,
            "soil_type": soil_type,
            "fertilization_method": fertilization_method,
            "farm_plan": farm_plan,
            "agent_reports": {
                "soil": soil,
                "weather": weather,
                "market": market,
                "finance": finance
            }
        }

        # Generate .docx and .pdf files
        try:
            file_paths = save_farm_plan_files(result)
            result["exported_files"] = file_paths
            print(f"Files saved: {file_paths['docx']}, {file_paths['pdf']}")
        except Exception:
            print("Could not export files (python-docx or fpdf2 may not be installed).")

        return result
    