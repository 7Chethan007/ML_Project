<?php
include 'db.php';

$company_id = $_GET['id'] ?? '';


$stmt = $conn->prepare("SELECT company_name, pros, cons, analysis_json FROM ml WHERE company_id = ?");
$stmt->bind_param("s", $company_id);
$stmt->execute();
$stmt->bind_result($company_name, $pros_json, $cons_json, $analysis_json);
$stmt->fetch();
$stmt->close();

$pros = json_decode($pros_json, true);
if (is_string($pros)) {
  $pros = array_filter(array_map('trim', preg_split('/\r?\n/', $pros)));
}
$cons = json_decode($cons_json, true);
if (is_string($cons)) {
  $cons = array_filter(array_map('trim', preg_split('/\r?\n/', $cons)));
}
$analysis = json_decode($analysis_json, true);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title><?= htmlspecialchars($company_name) ?> - ML Analysis</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { background-color: #f8f9fa; }
    .section-title { font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; }
    .pro-item, .con-item { padding: 8px; border-radius: 6px; margin-bottom: 6px; }
    .pro-item { background: #d4edda; color: #155724; }
    .con-item { background: #f8d7da; color: #721c24; }
    .card-custom { box-shadow: 0px 2px 6px rgba(0,0,0,0.1); }
  </style>
</head>
<body class="container mt-4">

  <a href="index.php" class="btn btn-secondary mb-3">← Back to All Companies</a>


  <div class="card card-custom p-4 mb-4">
    <h2 class="mb-4 text-primary">Analysis</h2>
    <!-- <p class="mb-2"># Analysis Generated Using ML</p> -->
    <div class="row g-3">
      <div class="col-md-4">
        <div class="p-3 border rounded h-100">
          <span class="fw-bold text-primary">Compounded Sales Growth</span><br>
          3 Years: <?= htmlspecialchars($analysis['compounded_sales_growth']['3'] ?? '-') ?><br>
          5 Years: <?= htmlspecialchars($analysis['compounded_sales_growth']['5'] ?? '-') ?><br>
          10 Years: <?= htmlspecialchars($analysis['compounded_sales_growth']['10'] ?? '-') ?>
        </div>
      </div>
      <div class="col-md-4">
        <div class="p-3 border rounded h-100">
          <span class="fw-bold text-primary">Compounded Profit Growth</span><br>
          3 Years: <?= htmlspecialchars($analysis['compounded_profit_growth']['3'] ?? '-') ?><br>
          5 Years: <?= htmlspecialchars($analysis['compounded_profit_growth']['5'] ?? '-') ?><br>
          10 Years: <?= htmlspecialchars($analysis['compounded_profit_growth']['10'] ?? '-') ?>
        </div>
      </div>
      <div class="col-md-4">
        <div class="p-3 border rounded h-100">
          <span class="fw-bold text-primary">Return on Equity</span><br>
          3 Years: <?= htmlspecialchars($analysis['roe']['3'] ?? '-') ?><br>
          5 Years: <?= htmlspecialchars($analysis['roe']['5'] ?? '-') ?><br>
          10 Years: <?= htmlspecialchars($analysis['roe']['10'] ?? '-') ?>
        </div>
      </div>
    </div>
  </div>

  <div class="card card-custom p-4">
    <h3 class="mb-2 text-primary">Pros and Cons</h3>
    <div class="mb-3"><span class="badge bg-secondary me-2" style="font-size:0.95em;"><i class="fa fa-circle me-1" style="font-size:0.7em;"></i>Generated Using Machine Learning</span></div>
    <div class="row g-3">
      <div class="col-md-6">
        <div class="p-3" style="background:#3ddad7; border-radius:16px; color:white;">
          <div class="fw-bold mb-2" style="font-size:1.3em;">Pros</div>
          <?php if (!empty($pros)): ?>
            <?php foreach ($pros as $pro): ?>
              <?php if (is_string($pro)): ?>
                <div class="mb-2"> <?= htmlspecialchars($pro) ?> </div>
              <?php endif; ?>
            <?php endforeach; ?>
          <?php else: ?>
            <p class="text-white-50">No pros available</p>
          <?php endif; ?>
        </div>
      </div>
      <div class="col-md-6">
        <div class="p-3" style="background:#ff5e8e; border-radius:16px; color:white;">
          <div class="fw-bold mb-2" style="font-size:1.3em;">Cons</div>
          <?php if (!empty($cons)): ?>
            <?php foreach ($cons as $con): ?>
              <?php if (is_string($con)): ?>
                <div class="mb-2"> <?= htmlspecialchars($con) ?> </div>
              <?php endif; ?>
            <?php endforeach; ?>
          <?php else: ?>
            <p class="text-white-50">No cons available</p>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
<?php
