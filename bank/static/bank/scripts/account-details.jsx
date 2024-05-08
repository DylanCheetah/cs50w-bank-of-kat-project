// Components
// ==========
function Transaction({date, description, source, dest, amount}) {
    return (
        <div className="row">
            <div className="col-2">{date}</div>
            <div className="col-2">{description}</div>
            <div className="col-3">{source}</div>
            <div className="col-3">{dest}</div>
            <div className="col-2">${amount}</div>
        </div>
    );
}


function BusyIndicator({visible}) {
    if(visible) {
        return (
            <div className="row justify-content-center">
                <div className="col-2 spinner-border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    } else {
        return (
            <div></div>
        );
    }
}


function Root() {
    // Initialize states
    let [busy, setBusy] = React.useState(true);
    let [start, setStart] = React.useState(0);
    let [transactions, setTransactions] = React.useState([]);

    // Load info for first 20 transactions if no transactions are loaded
    if(!transactions.length) {
        const accountId = document.querySelector("#root").dataset.account_id;

        fetch(`/transactions?account_id=${accountId}&start=0&count=20`)
        .then((response) => response.json())
        .then((data) => {
            // Return if there are no transactions
            if(!data.transactions.length) {
                setBusy(false);
                return;
            }

            // Display transaction data
            setStart(start + 20);
            setTransactions(data.transactions.map((transaction) => {
                return (
                    <Transaction date={transaction.date} description={transaction.description} source={transaction.source} dest={transaction.dest} amount={transaction.amount} />
                );
            }));
            setBusy(false);
        })
        .catch((error) => {
            alert(error);
        });
    }

    // Add event listener for scrolling
    window.onscroll = (event) => {
        // Load more content?
        if(window.scrollY == document.body.clientHeight - window.innerHeight) {
            const accountId = document.querySelector("#root").dataset.account_id;
            setBusy(true);
            setStart(start + 20);

            fetch(`/transactions?account_id=${accountId}&start=${start}&count=20`)
            .then((response) => response.json())
            .then((data) => {
                // Return if there is no additional transaction data
                if(!data.transactions.length) {
                    setBusy(false);
                    return;
                }

                // Display more transaction data
                let newTransactions = data.transactions.map((transaction) => {
                    return (
                        <Transaction date={transaction.date} description={transaction.description} source={transaction.source} dest={transaction.dest} amount={transaction.amount} />
                    );
                });
                setTransactions([...transactions, ...newTransactions]);
                setBusy(false);
            })
            .catch((error) => {
                alert(error);
            });
        }
    };

    return (
        <div>
            <div className="row bg-light border">
                <strong className="col-2">Date</strong>
                <strong className="col-2">Desc.</strong>
                <strong className="col-3">Source</strong>
                <strong className="col-3">Dest.</strong>
                <strong className="col-2">Amount</strong>
            </div>
            {transactions}
            <BusyIndicator visible={busy} />
        </div>
    );
}


// Create root
const root = ReactDOM.createRoot(document.querySelector("#root"));
root.render(<Root />);
