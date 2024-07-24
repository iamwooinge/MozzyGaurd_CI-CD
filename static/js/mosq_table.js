document.addEventListener('DOMContentLoaded', function () {
    const mosqIndexSpan = document.getElementById('mosq_index');
    const tableDiv = document.getElementById('table');

    function generateTable(mosqIndex) {
        let tableHTML = '<table class="table table-striped">';
        tableHTML += '<thead><tr><th class="index-header">Index</th><th>개인 - 실내</th><th>개인 - 실외</th><th>기관/사회</th> </thead>';
        tableHTML += '<tbody>';

        if (mosqIndex === 0) {
            tableHTML += `
                <tr>
                    <td rowspan="2">1단계<br><br>0이상 25미만</td>
                    <td>창문과 문에 방충망 사용 </td>
                    <td>별도의 모기 방제방법이 필요하지 않음</td>
                    <td>월동모기 방제</td>
                </tr>
                <tr>
                    <td>        </td>
                    <td>        </td>
                    <td>모기유충 서식지 파악 및 감시</td>
                </tr>
            `;
        } else if (mosqIndex === 1) {
            tableHTML += `
                <tr>
                    <td rowspan="4">2단계 <br><br>25이상 50미만</td>
                    <td>쾌적 단계 행동 유지 </td>
                    <td>생활 주변의 방치된 용기 물 비우기</td>
                    <td>지역별로 물이 고일 수 있는 시설 및 부품 제거하기 </td>
                </tr>
                <tr>
                    <td>늦은 시간 환기 자제</td>
                    <td>주택 옥상의 빗물 통에 뚜껑 설치</td>
                    <td>모기 유충 서식 방제 및 관리</td>
                </tr>
                <tr>
                    <td>방충망 하자 등 침입 가능 통로 보수</td>
                    <td>단독주택 정화조 환기구에 모기망 설치</td>
                    <td>모기 성충 발생 모니터링</td>
                </tr>
                <tr>
                    <td>정화조의 금이나 틈새 확인 및 수리</td>
                    <td>       </td>
                    <td>       </td>
                </tr>
            `;
        } else if (mosqIndex === 2) {
            tableHTML += `
                <tr>
                    <td rowspan="8">3단계 <br><br>50이상 75미만</td>
                    <td>관심 단계 행동 유지</td>
                    <td>관심 단계 행동 유지</td>
                    <td>야외 모기 유충 방제</td>
                </tr>
                <tr>
                    <td>출입문과 창문을 열어 환기하는 것을 자제</td>
                    <td>물이 고인 용기는 비우고 뒤집어 놓기</td>
                    <td>모기 성충 발생 모니터링</td>
                </tr>
                <tr>
                    <td>아기침대에 모기장 사용</td>
                    <td>집주변에 (화초나 풀이 무성하게 자란 곳, 보일러 실, 창고, 그늘진 곳, 지하계단 등)에서 모기가 발견 시 가정용 에어로졸로 방제</td>
                    <td>버려진 세탁기, 냉장고, 변기와 같이 물이 쌓일 수 있는 폐기물 방치 관리</td>
                </tr>
                <tr>
                    <td>        </td>
                    <td>야외 활동 시 피부 노출 최소화하기</td>
                    <td>방제 모기 성충 발생밀도 감시</td>
                </tr>
                <tr>
                    <td>        </td>
                    <td>유모차에 모기장 사용</td>
                    <td>모기의 수와 분포에 대해 조사하고, 유충서식지 제거에 대한 영향력을 평가</td>
                </tr>
                <tr>
                    <td>오후 7시 이후 출입문, 창문(방충망 없는) 열어 놓지 않도록 주의</td>
                    <td>야간 활동 시 어린이는 어린이 전용 모기기피제 사용 (주의사항 반드시 확인)</td>
                    <td>        </td>
                </tr>
                <tr>
                    <td>        </td>
                    <td>야외 활동 시 모기기피제 사용(사용 전 주의사항을 반드시 확인해야 하며, 어린이는 어린이 전용 모기기피제 사용)</td>
                    <td>        </td>
                </tr>
                <tr>
                    <td>        </td>
                    <td>야외에서 대규모 야외 모기 서식지를 확인할 경우 보건소에 신고</td>
                    <td>        </td>
                </tr>
            `;
        } else if (mosqIndex === 3) {
            tableHTML += `
                <tr>
                    <td rowspan="8">4단계 <br><br>75이상</td>
                    <td>주의 단계 행동 유지</td>
                    <td>주의 단계 행동 유지</td>
                    <td>민원 발생지역 적극 조사</td>
                </tr>
                <tr>
                    <td>취침 시 모기장 사용</td>
                    <td>야간 활동 시 반드시 모기기피제 사용</td>
                    <td>모기 성충 발생 모니터링</td>
                </tr>
                <tr>
                    <td>출입문 주변에 가정용 살충제 처리</td>
                    <td>야간 활동 자제</td>
                    <td>상하수도 정비, 재활용수거함 정비, 재활용 타이어 적치에 대한 방안 강구</td>
                </tr>
                <tr>
                    <td>야외 활동 후 바로 샤워하기</td>
                    <td>일상생활에서 볼 수 있는 모기 발생원 적극 제거</td>
                    <td>        </td>
                </tr>
                <tr>
                    <td>모기 발견 시 즉각 에어로졸 방제</td>
                    <td>하룻밤 주택 내 모기 5마리 이상 침입 시 관할 보건소 방역기동반에 알리기</td>
                    <td>        </td>
                </tr>
                <tr>
                    <td>취침 2시간 전 전자모기향을 사용하고, 사용을 종료한 후 반드시 환기한 후 취침하기</td>
                    <td>일상생활에서 볼 수 있는 모기 발생원 적극 제거</td>
                    <td>        </td>
                </tr>
                <tr>
                    <td>취침 전 샤워하기</td>
                    <td>        </td>
                    <td>        </td>
                </tr>
            `;
        } else {
            tableHTML += '<tr><td colspan="3">No data available</td></tr>';
        }

        tableHTML += '</tbody></table>';
        return tableHTML;
    }

    function updateTable() {
        const textContent = mosqIndexSpan.textContent.trim();
        //console.log(`textContent: '${textContent}'`); // This will show the content of the element

        const mosqIndex = isNaN(parseInt(textContent, 10)) ? NaN : parseInt(textContent, 10);
        //console.log(`mosqIndex: ${mosqIndex}`); // This will show the parsed integer or NaN

        const tableHTML = generateTable(mosqIndex);
        tableDiv.innerHTML = tableHTML;
    }

    // Observe changes to the mosq_index element
    const observer = new MutationObserver(updateTable);
    observer.observe(mosqIndexSpan, { childList: true, characterData: true, subtree: true });

    // Initial table update
    updateTable();

});
