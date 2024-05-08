
// Components
// ==========
function Account({id, number, type, balance, maturity}) {
    let url = `/account/${id}`;
    return (
        <div className="row">
            <a className="col-3" href={url} style={{"text-decoration": "none"}}>{number}</a>
            <div className="col-3">{type}</div>
            <div className="col-3">${balance}</div>
            <div className="col-3">{maturity}</div>
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
    // Create component states
    let [busy, setBusy] = React.useState(true);
    let [start, setStart] = React.useState(0);
    let [accounts, setAccounts] = React.useState([]);

    // Load info for first 10 accounts if no account data loaded
    if(!accounts.length) {
        fetch(`/account/get?start=0&count=20`)
        .then((response) => response.json())
        .then((data) => {
            // Return if there is no account data
            if(!data.accounts.length) {
                setBusy(false);
                return;
            }

            // Display account data
            setStart(start + 20);
            setAccounts(data.accounts.map((account) => {
                return (
                    <Account id={account.id} number={account.number} type={account.type} balance={account.balance} maturity={account.maturity} />
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
            setBusy(true);
            fetch(`/account/get?start=${start}&count=20`)
            .then((response) => response.json())
            .then((data) => {
                // Return if there is no more account data
                if(!data.accounts.length) {
                    setBusy(false);
                    return;
                }

                // Display additional account data
                let newAccounts = data.accounts.map((account) => {
                    return (
                        <Account id={account.id} number={account.number} type={account.type} balance={account.balance} maturity={account.maturity} />
                    );
                });
                setStart(start + 20);
                setAccounts([...accounts, ...newAccounts]);
                setBusy(false);
            })
            .catch((error) => {
                alert(error);
            });
        }
    };

    return (
        <div>
            <div className="row border">
                <strong className="col-3 bg-light">No.</strong>
                <strong className="col-3 bg-light">Type</strong>
                <strong className="col-3 bg-light">Balance</strong>
                <strong className="col-3 bg-light">Maturity</strong>
            </div>
            <div className="row justify-content-center">
                {accounts}
            </div>
            <BusyIndicator visible={busy} />
        </div>
    );
}


// Create root
const root = ReactDOM.createRoot(document.querySelector("#root"));
root.render(<Root />);
