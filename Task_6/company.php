<?php
include 'db.php';

$company_id = $_GET['id'] ?? '';

$stmt = $conn->prepare("SELECT company_name, pros, cons FROM ml WHERE company_id = ?");
$stmt->bind_param("s", $company_id);
$stmt->execute();
$stmt->bind_result($company_name, $pros_json, $cons_json);
$stmt->fetch();
$stmt->close();

$pros = json_decode($pros_json, true);
$cons = json_decode($cons_json, true);
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

  <div class="card card-custom p-4">
    <h2 class="mb-4"><?= htmlspecialchars($company_name) ?> - ML Insights</h2>

    <div class="row">
      <!-- Pros -->
      <div class="col-md-6">
        <div class="section-title text-success"><i class="fa fa-thumbs-up"></i> Pros</div>
        <?php if (!empty($pros)): ?>
          <?php foreach ($pros as $pro): ?>
            <div class="pro-item"><i class="fa fa-check-circle"></i> <?= htmlspecialchars($pro['text']) ?></div>
          <?php endforeach; ?>
        <?php else: ?>
          <p class="text-muted">No pros available</p>
        <?php endif; ?>
      </div>

      <!-- Cons -->
      <div class="col-md-6">
        <div class="section-title text-danger"><i class="fa fa-thumbs-down"></i> Cons</div>
        <?php if (!empty($cons)): ?>
          <?php foreach ($cons as $con): ?>
            <div class="con-item"><i class="fa fa-times-circle"></i> <?= htmlspecialchars($con['text']) ?></div>
          <?php endforeach; ?>
        <?php else: ?>
          <p class="text-muted">No cons available</p>
        <?php endif; ?>
      </div>
    </div>
  </div>

</body>
</html>
<?php
